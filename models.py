"""
Database Models for DropBy.HOLLOW
"""

from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import json


class Category(db.Model):
    """Category model for product categories."""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'image_url': self.image_url,
            'description': self.description,
            'product_count': len(self.products) if self.products else 0
        }


class Product(db.Model):
    """Product model for items in the store."""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    source_urls = db.Column(db.Text, nullable=True)  # JSON string of source URLs
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    orders = db.relationship('Order', backref='product', lazy=True)
    
    def set_source_urls(self, urls):
        """Set source URLs as JSON string."""
        self.source_urls = json.dumps(urls)
    
    def get_source_urls(self):
        """Get source URLs as list."""
        if self.source_urls:
            return json.loads(self.source_urls)
        return []
    
    def get_final_price(self, source_price=None):
        """Calculate final price with service fee."""
        from flask import current_app
        service_fee = current_app.config.get('SERVICE_FEE', 20.00)
        if source_price:
            return round(source_price + service_fee, 2)
        return round(self.base_price + service_fee, 2)
    
    def to_dict(self, include_sources=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'base_price': self.base_price,
            'image_url': self.image_url,
            'final_price': self.get_final_price(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_sources:
            data['source_urls'] = self.get_source_urls()
        return data


class Order(db.Model):
    """Order model for customer purchases."""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # Customer information
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(50), nullable=True)
    shipping_address = db.Column(db.Text, nullable=False)
    
    # Product information
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_image = db.Column(db.String(500), nullable=True)
    source_url = db.Column(db.String(1000), nullable=True)  # CRITICAL: Source URL for admin
    selected_price = db.Column(db.Float, nullable=False)
    service_fee = db.Column(db.Float, nullable=False)
    final_price = db.Column(db.Float, nullable=False)
    
    # Payment information
    payment_status = db.Column(db.String(50), default='pending')  # pending, paid, failed
    payment_intent_id = db.Column(db.String(100), nullable=True)
    stripe_customer_id = db.Column(db.String(100), nullable=True)
    
    # Order status
    status = db.Column(db.String(50), default='pending')  # pending, purchased, shipped, delivered, cancelled
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    
    def generate_order_number(self):
        """Generate unique order number."""
        import random
        import string
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f'DH-{timestamp}-{random_suffix}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'shipping_address': self.shipping_address,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_image': self.product_image,
            'source_url': self.source_url,  # CRITICAL for admin
            'selected_price': self.selected_price,
            'service_fee': self.service_fee,
            'final_price': self.final_price,
            'payment_status': self.payment_status,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None
        }
    
    def to_admin_notification(self):
        """Format order for admin notification."""
        return f"""
🔔 NEW ORDER - {self.order_number}

👤 CUSTOMER INFO:
   Name: {self.customer_name}
   Email: {self.customer_email}
   Phone: {self.customer_phone or 'N/A'}
   
📍 SHIPPING ADDRESS:
   {self.shipping_address}

🛍️ PRODUCT DETAILS:
   Product: {self.product_name}
   Base Price: ${self.selected_price:.2f}
   Service Fee: ${self.service_fee:.2f}
   Total Paid: ${self.final_price:.2f}
   
🔗 SOURCE LINK (CRITICAL):
   {self.source_url or 'No source URL available'}
   
💳 PAYMENT:
   Status: {self.payment_status}
   Payment ID: {self.payment_intent_id or 'N/A'}

🕐 Order placed: {self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else 'N/A'}
"""


class PriceSource(db.Model):
    """Model to store scraped prices from various sources."""
    __tablename__ = 'price_sources'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    source_name = db.Column(db.String(100), nullable=False)
    source_url = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'source_name': self.source_name,
            'source_url': self.source_url,
            'price': self.price,
            'final_price': round(self.price + 20.00, 2),  # Add service fee
            'in_stock': self.in_stock,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }


class User(db.Model):
    """User model for authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Set hashed password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

