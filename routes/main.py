"""
Main Routes for DropBy.HOLLOW
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from models import Category, Product, Order, PriceSource
from config import Config
from routes.auth import login_required


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Home page with categories."""
    categories = Category.query.all()
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    return render_template("index.html", 
                           categories=categories, 
                           featured_products=featured_products)


@main_bp.route("/category/<slug>")
def category(slug):
    """Category page showing products."""
    category = Category.query.filter_by(slug=slug).first_or_404()
    products = Product.query.filter_by(category_id=category.id, is_active=True).all()
    return render_template("category.html", category=category, products=products)


@main_bp.route("/product/<int:product_id>")
def product(product_id):
    """Product detail page with price aggregation."""
    product = Product.query.get_or_404(product_id)
    price_sources = PriceSource.query.filter_by(product_id=product.id, in_stock=True).all()
    
    sources_with_final_price = []
    for source in price_sources:
        source_data = source.to_dict()
        source_data["final_price"] = round(source.price + Config.SERVICE_FEE, 2)
        sources_with_final_price.append(source_data)
    
    return render_template("product.html", 
                           product=product, 
                           price_sources=sources_with_final_price,
                           service_fee=Config.SERVICE_FEE)


@main_bp.route("/checkout/<int:product_id>", methods=["GET", "POST"])
@login_required
def checkout(product_id):
    """Checkout page - requires login."""
    product = Product.query.get_or_404(product_id)
    
    source_url = request.args.get("source_url", "")
    selected_price = float(request.args.get("price", product.base_price))
    final_price = round(selected_price + Config.SERVICE_FEE, 2)
    
    if request.method == "POST":
        order = Order(
            order_number="",
            customer_name=request.form.get("customer_name"),
            customer_email=request.form.get("customer_email"),
            customer_phone=request.form.get("customer_phone"),
            shipping_address=request.form.get("shipping_address"),
            product_id=product.id,
            product_name=product.title,
            product_image=product.image_url,
            source_url=source_url,
            selected_price=selected_price,
            service_fee=Config.SERVICE_FEE,
            final_price=final_price,
            payment_status="pending",
            status="pending"
        )
        order.order_number = order.generate_order_number()
        
        db.session.add(order)
        db.session.commit()
        
        session["pending_order_id"] = order.id
        
        return redirect(url_for("main.payment", order_id=order.id))
    
    return render_template("checkout.html", 
                           product=product,
                           source_url=source_url,
                           selected_price=selected_price,
                           final_price=final_price,
                           service_fee=Config.SERVICE_FEE)


@main_bp.route("/payment/<int:order_id>", methods=["GET", "POST"])
def payment(order_id):
    """Payment page with Stripe."""
    order = Order.query.get_or_404(order_id)
    
    if request.method == "POST":
        order.payment_status = "paid"
        order.paid_at = db.func.now()
        db.session.commit()
        
        send_admin_notification(order)
        
        session.pop("pending_order_id", None)
        
        return redirect(url_for("main.success", order_id=order.id))
    
    return render_template("payment.html", order=order, stripe_key=Config.STRIPE_PUBLISHABLE_KEY)


@main_bp.route("/success/<int:order_id>")
def success(order_id):
    """Order success page."""
    order = Order.query.get_or_404(order_id)
    return render_template("success.html", order=order)


@main_bp.route("/cart")
def cart():
    """Shopping cart page."""
    cart_items = session.get("cart", [])
    return render_template("cart.html", cart_items=cart_items)


def send_admin_notification(order):
    """Send notification to admin about new order."""
    notification = order.to_admin_notification()
    print("\n" + "="*50)
    print("NEW ORDER RECEIVED - DropBy.HOLLOW")
    print("="*50)
    print(notification)
    print("="*50 + "\n")

