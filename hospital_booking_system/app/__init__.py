from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Login required'
    mail.init_app(app)
    migrate.init_app(app, db)
    
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Blueprints
    from .routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from .routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .routes.patient import bp as patient_bp
    app.register_blueprint(patient_bp, url_prefix='/patient')
    
    from .routes.doctor import bp as doctor_bp
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    
    from .routes.staff import bp as staff_bp
    app.register_blueprint(staff_bp, url_prefix='/staff')
    
    from .routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app


