"""
Admin Routes for DropBy.HOLLOW
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app import db
from models import Order, Product, Category
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def dashboard():
    """Admin dashboard."""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    paid_orders = Order.query.filter_by(payment_status='paid').count()
    
    return render_template('admin/dashboard.html',
                           orders=orders,
                           total_orders=total_orders,
                           pending_orders=pending_orders,
                           paid_orders=paid_orders)


@admin_bp.route('/orders')
def orders():
    """Order management page."""
    status_filter = request.args.get('status', '')
    payment_filter = request.args.get('payment_status', '')
    
    query = Order.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    if payment_filter:
        query = query.filter_by(payment_status=payment_filter)
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    return render_template('admin/orders.html', orders=orders)


@admin_bp.route('/orders/<int:order_id>')
def order_detail(order_id):
    """Order detail page."""
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)


@admin_bp.route('/orders/<int:order_id>/update', methods=['POST'])
def update_order(order_id):
    """Update order status."""
    order = Order.query.get_or_404(order_id)
    
    status = request.form.get('status')
    payment_status = request.form.get('payment_status')
    
    if status:
        order.status = status
        if status == 'purchased':
            order.shipped_at = datetime.utcnow()
        elif status == 'shipped':
            order.shipped_at = datetime.utcnow()
        elif status == 'delivered':
            order.delivered_at = datetime.utcnow()
    
    if payment_status:
        order.payment_status = payment_status
        if payment_status == 'paid' and not order.paid_at:
            order.paid_at = datetime.utcnow()
    
    db.session.commit()
    flash(f'Order {order.order_number} updated successfully!', 'success')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))


@admin_bp.route('/orders/<int:order_id>/delete', methods=['POST'])
def delete_order(order_id):
    """Delete an order."""
    order = Order.query.get_or_404(order_id)
    order_number = order.order_number
    
    db.session.delete(order)
    db.session.commit()
    
    flash(f'Order {order_number} deleted successfully!', 'success')
    return redirect(url_for('admin.orders'))


@admin_bp.route('/products')
def products():
    """Product management page."""
    category_id = request.args.get('category_id', type=int)
    
    query = Product.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.order_by(Product.created_at.desc()).all()
    categories = Category.query.all()
    
    return render_template('admin/products.html', 
                           products=products, 
                           categories=categories)


@admin_bp.route('/scrape/<int:product_id>', methods=['POST'])
def scrape_product(product_id):
    """Trigger scraping for a product."""
    flash(f'Scraping initiated for product {product_id}', 'info')
    return redirect(url_for('admin.products'))


@admin_bp.route('/api/orders')
def api_orders():
    """Get orders as JSON for AJAX."""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([order.to_dict() for order in orders])


@admin_bp.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def api_update_status(order_id):
    """Update order status via API."""
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    order.status = data.get('status', order.status)
    
    if order.status == 'purchased':
        order.shipped_at = datetime.utcnow()
    elif order.status == 'shipped':
        order.shipped_at = datetime.utcnow()
    elif order.status == 'delivered':
        order.delivered_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'order': order.to_dict()
    })
