from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.utils import role_required
from app.models import Appointment, User
from app import db
from datetime import datetime

bp = Blueprint('staff', __name__)

@bp.route('/dashboard')
@login_required
@role_required('staff')
def dashboard():
    appts = Appointment.query.filter(Appointment.date_time > datetime.utcnow()).all()
    return render_template('staff/dashboard.html', appointments=appts)

@bp.route('/approve/<int:appt_id>')
@login_required
@role_required('staff')
def approve(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    if appt.status == 'pending':
        appt.status = 'confirmed'
        # Could log revenue here if paid
        db.session.commit()
        flash('Appointment approved')
    return redirect(url_for('staff.dashboard'))

@bp.route('/cancel/<int:appt_id>')
@login_required
@role_required('staff')
def staff_cancel(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = 'cancelled'
    db.session.commit()
    flash('Appointment cancelled')
    return redirect(url_for('staff.dashboard'))

