from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.utils import role_required
from app.models import Appointment, Doctor, RevenueLog
from app import db
from datetime import datetime

bp = Blueprint('doctor', __name__)

@bp.route('/dashboard')
@login_required
@role_required('doctor')
def dashboard():
    doctor_profile = Doctor.query.filter_by(user_id=current_user.id).first()
    if not doctor_profile:
        flash('Complete your doctor profile first')
        return redirect(url_for('main.index'))
    
    upcoming = Appointment.query.filter(
        Appointment.doctor_id == doctor_profile.id,
        Appointment.date_time > datetime.utcnow(),
        Appointment.status == 'pending'
    ).all()
    
    confirmed = Appointment.query.filter(
        Appointment.doctor_id == doctor_profile.id,
        Appointment.date_time > datetime.utcnow(),
        Appointment.status == 'confirmed'
    ).all()
    
    return render_template('doctor/dashboard.html', upcoming=upcoming, confirmed=confirmed, doctor=doctor_profile)

@bp.route('/confirm/<int:appt_id>')
@login_required
@role_required('doctor')
def confirm_appt(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    doctor_profile = Doctor.query.filter_by(user_id=current_user.id).first()
    if appt.doctor_id == doctor_profile.id and appt.status == 'pending':
        appt.status = 'confirmed'
        # Log revenue
        revenue = RevenueLog(appointment_id=appt.id, doctor_id=current_user.id, amount=appt.fee)
        db.session.add(revenue)
        db.session.commit()
        flash('Appointment confirmed, revenue logged')
    return redirect(url_for('doctor.dashboard'))

