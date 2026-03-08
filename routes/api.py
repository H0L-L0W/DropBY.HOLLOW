"""
API Routes for DropBy.HOLLOW
"""

from flask import Blueprint, jsonify, request
from app import db
from models import Category, Product, Order, PriceSource
from config import Config
import json
from datetime import datetime

api_bp = Blueprint('api', __name__)


@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories."""
    categories = Category.query.all()
    return jsonify([cat.to_dict() for cat in categories])


@api_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get single category."""
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict())


@api_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional filters."""
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(Product.title.ilike(f'%{search}%'))
    
    products = query.all()
    return jsonify([prod.to_dict() for prod in products])


@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product with price sources."""
    product = Product.query.get_or_404(product_id)
    price_sources = PriceSource.query.filter_by(product_id=product.id).all()
    
    result = product.to_dict()
    result['price_sources'] = [ps.to_dict() for ps in price_sources]
    return jsonify(result)


@api_bp.route('/products/<int:product_id>/scrape', methods=['POST'])
def scrape_product(product_id):
    """Trigger price scraping for a product."""
    product = Product.query.get_or_404(product_id)
    
    # In production, this would trigger actual scraping
    # For now, we'll return mock data
    mock_sources = generate_mock_sources(product)
    
    # Save price sources to database
    for source in mock_sources:
        price_source = PriceSource(
            product_id=product.id,
            source_name=source['source_name'],
            source_url=source['source_url'],
            price=source['price'],
            in_stock=source['in_stock']
        )
        db.session.add(price_source)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'product_id': product_id,
        'sources': mock_sources
    })


def generate_mock_sources(product):
    """Generate mock price sources for demonstration."""
    import random
    sources = [
        'Amazon', 'eBay', 'AliExpress', 'Walmart', 'Target',
        'Best Buy', 'Newegg', 'Etsy', 'Overstock', 'Wish'
    ]
    
    result = []
    for source in sources[:8]:
        base_variance = random.uniform(0.85, 1.15)
        price = round(product.base_price * base_variance, 2)
        
        result.append({
            'source_name': source,
            'source_url': f'https://{source.lower().replace(" ", "")}.com/product/{product.id}',
            'price': price,
            'in_stock': random.choice([True, True, True, False])
        })
    
    return result


@api_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order."""
    data = request.get_json()
    
    order = Order(
        order_number='',
        customer_name=data.get('customer_name'),
        customer_email=data.get('customer_email'),
        customer_phone=data.get('customer_phone', ''),
        shipping_address=data.get('shipping_address'),
        product_id=data.get('product_id'),
        product_name=data.get('product_name'),
        product_image=data.get('product_image', ''),
        source_url=data.get('source_url'),
        selected_price=data.get('selected_price'),
        service_fee=Config.SERVICE_FEE,
        final_price=data.get('final_price'),
        payment_status='pending',
        status='pending'
    )
    order.order_number = order.generate_order_number()
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'order': order.to_dict()
    })


@api_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details."""
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())


@api_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status."""
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    order.status = data.get('status', order.status)
    
    if order.status == 'shipped':
        order.shipped_at = datetime.utcnow()
    elif order.status == 'delivered':
        order.delivered_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'order': order.to_dict()
    })


@api_bp.route('/payment/create-intent', methods=['POST'])
def create_payment_intent():
    """Create Stripe payment intent."""
    data = request.get_json()
    amount = int(data.get('amount', 0) * 100)
    
    # Mock response for demo
    return jsonify({
        'clientSecret': 'pi_mock_secret_' + str(datetime.utcnow().timestamp())
    })


@api_bp.route('/payment/webhook', methods=['POST'])
def payment_webhook():
    """Handle Stripe webhook."""
    data = request.get_json()
    if data.get('type') == 'payment_intent.succeeded':
        order_id = data.get('data', {}).get('metadata', {}).get('order_id')
        if order_id:
            order = Order.query.get(order_id)
            if order:
                order.payment_status = 'paid'
                order.paid_at = datetime.utcnow()
                db.session.commit()
    
    return jsonify({'success': True})
