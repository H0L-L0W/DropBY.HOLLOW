"""
DropBy.HOLLOW - E-Commerce Aggregator
Main Flask Application
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from config import config
from extensions import db
import os
import json
from datetime import datetime


def create_app(config_name='default'):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from routes.main import main_bp
    from routes.api import api_bp
    from routes.admin import admin_bp
    from routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # Initialize sample data if empty
        initialize_sample_data()
    
    return app


def initialize_sample_data():
    """Initialize sample categories and products."""
    from models import Category, Product
    
    if Category.query.count() == 0:
        # Create categories
        categories = [
            {'name': 'Gaming', 'slug': 'gaming', 'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600&h=400&fit=crop', 'description': 'Premium gaming equipment and accessories'},
            {'name': 'Artisan Accessories', 'slug': 'artisan-accessories', 'image_url': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=600&h=400&fit=crop', 'description': 'Handcrafted luxury accessories'},
            {'name': 'Perfumes', 'slug': 'perfumes', 'image_url': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=600&h=400&fit=crop', 'description': 'Exclusive fragrances from top brands'},
            {'name': 'Cosmetics', 'slug': 'cosmetics', 'image_url': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&h=400&fit=crop', 'description': 'Premium beauty and skincare products'}
        ]
        
        for cat_data in categories:
            category = Category(**cat_data)
            db.session.add(category)
        
        db.session.commit()
        
        # Create sample products for each category
        sample_products = [
            # Gaming
            {'title': 'Premium Gaming Headset', 'description': 'High-fidelity audio with noise cancellation and surround sound', 'category_id': 1, 'base_price': 149.99, 'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop'},
            {'title': 'Mechanical Gaming Keyboard', 'description': 'RGB backlit mechanical switches with programmable macros', 'category_id': 1, 'base_price': 179.99, 'image_url': 'https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400&h=400&fit=crop'},
            {'title': 'Pro Gaming Mouse', 'description': 'Precision optical sensor with customizable weight system', 'category_id': 1, 'base_price': 89.99, 'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop'},
            {'title': '4K Gaming Monitor', 'description': '144Hz refresh rate with HDR support', 'category_id': 1, 'base_price': 599.99, 'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop'},
            {'title': 'Gaming Controller', 'description': 'Wireless controller with haptic feedback', 'category_id': 1, 'base_price': 69.99, 'image_url': 'https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400&h=400&fit=crop'},
            
            # Artisan Accessories
            {'title': 'Handcrafted Leather Wallet', 'description': 'Genuine Italian leather with RFID protection', 'category_id': 2, 'base_price': 129.99, 'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=400&fit=crop'},
            {'title': 'Artisan Watch', 'description': 'Swiss movement with sapphire crystal', 'category_id': 2, 'base_price': 449.99, 'image_url': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=400&fit=crop'},
            {'title': 'Handwoven Silk Scarf', 'description': '100% organic silk with traditional patterns', 'category_id': 2, 'base_price': 189.99, 'image_url': 'https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400&h=400&fit=crop'},
            {'title': 'Custom Belt', 'description': 'Hand-stitched with brass buckle', 'category_id': 2, 'base_price': 99.99, 'image_url': 'https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=400&h=400&fit=crop'},
            {'title': 'Leather Messenger Bag', 'description': 'Vintage style with modern functionality', 'category_id': 2, 'base_price': 279.99, 'image_url': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop'},
            
            # Perfumes
            {'title': 'Luxury Eau de Parfum', 'description': 'Long-lasting fragrance with notes of oud and sandalwood', 'category_id': 3, 'base_price': 249.99, 'image_url': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=400&fit=crop'},
            {'title': 'Floral Essence Spray', 'description': 'Delicate rose and jasmine blend', 'category_id': 3, 'base_price': 179.99, 'image_url': 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=400&h=400&fit=crop'},
            {'title': 'Citrus Fresh Cologne', 'description': 'Refreshing bergamot and lemon scent', 'category_id': 3, 'base_price': 129.99, 'image_url': 'https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=400&h=400&fit=crop'},
            {'title': 'Vanilla Dream Perfume', 'description': 'Warm vanilla with amber undertones', 'category_id': 3, 'base_price': 159.99, 'image_url': 'https://images.unsplash.com/photo-1594035910387-fea47794261f?w=400&h=400&fit=crop'},
            {'title': 'Woody Signature Scent', 'description': 'Cedar and vetiver for men', 'category_id': 3, 'base_price': 199.99, 'image_url': 'https://images.unsplash.com/photo-1523293188086-b431e93f9e77?w=400&h=400&fit=crop'},
            
            # Cosmetics
            {'title': 'Premium Skincare Set', 'description': 'Anti-aging serum and moisturizer duo', 'category_id': 4, 'base_price': 189.99, 'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop'},
            {'title': 'Luxury Lipstick Collection', 'description': 'Matte and satin finish set', 'category_id': 4, 'base_price': 79.99, 'image_url': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400&h=400&fit=crop'},
            {'title': 'Professional Makeup Palette', 'description': '24-color eyeshadow palette', 'category_id': 4, 'base_price': 129.99, 'image_url': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=400&fit=crop'},
            {'title': 'Hydrating Face Mask Set', 'description': '5 different sheet masks', 'category_id': 4, 'base_price': 49.99, 'image_url': 'https://images.unsplash.com/photo-1570194065650-d99fb4b38b15?w=400&h=400&fit=crop'},
            {'title': 'High-End Foundation', 'description': 'Full coverage with skincare benefits', 'category_id': 4, 'base_price': 89.99, 'image_url': 'https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400&h=400&fit=crop'}
        ]
        
        for prod_data in sample_products:
            product = Product(**prod_data)
            db.session.add(product)
        
        db.session.commit()
        print("Sample data initialized successfully!")


if __name__ == '__main__':
    # Check if running on Render (production)
    config_name = 'production' if os.environ.get('RENDER') else 'development'
    app = create_app(config_name)
    app.run(debug=(config_name == 'development'), host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
