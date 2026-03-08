"""
Authentication Routes for DropBy.HOLLOW
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from models import User
from functools import wraps

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration."""
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not email or not name or not password:
            flash('All fields are required.', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('signup.html')
        
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return render_template('signup.html')
        
        # Create new user
        user = User(email=email, name=name)
        user.set_password(password)
        
        # First user is admin
        if User.query.count() == 0:
            user.is_admin = True
        
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['is_admin'] = user.is_admin
            
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to previous page or home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

