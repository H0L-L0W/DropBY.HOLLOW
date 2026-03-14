from flask import Blueprint, render_template
from flask_login import login_required
from app.utils import role_required
from app.models import User, RevenueLog, Appointment, Doctor
from app import db
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    total_users = User.query.count()
    total_appts = Appointment.query.count()
    total_revenue = db.session.query(db.func.sum(RevenueLog.amount)).scalar() or 0
    doctors = Doctor.query.all()
    return render_template('admin/dashboard.html', stats={
        'total_users': total_users,
        'total_appts': total_appts,
        'total_revenue': total_revenue,
        'doctors': doctors
    })

@bp.route('/analytics')
@login_required
@role_required('admin')
def analytics():
    # Weekly revenue etc.
    week_revenue = db.session.query(db.func.sum(RevenueLog.amount)).filter(
        RevenueLog.timestamp > datetime.utcnow() - timedelta(days=7)
    ).scalar() or 0
    return render_template('admin/analytics.html', week_revenue=week_revenue)

