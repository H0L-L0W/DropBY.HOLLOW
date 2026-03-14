from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import BookingForm
from app.models import Appointment, Doctor, Department
from app.utils import role_required, is_available
from app import db
from datetime import datetime, timedelta

bp = Blueprint('patient', __name__)

@bp.route('/dashboard')
@login_required
@role_required('patient')
def dashboard():
    upcoming = Appointment.query.filter(
        Appointment.patient_id == current_user.id,
        Appointment.date_time > datetime.utcnow()
    ).all()
    past = Appointment.query.filter(
        Appointment.patient_id == current_user.id,
        Appointment.date_time <= datetime.utcnow()
    ).all()
    return render_template('patient/dashboard.html', upcoming=upcoming, past=past)

@bp.route('/book', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def book():
    form = BookingForm()
    departments = Department.query.all()
    doctors = []
    for dept in departments:
        doctors += dept.doctors.all()
    form.doctor_id.choices = [(0, 'Select Doctor')] + [(d.id, d.user.first_name + ' ' + d.user.last_name + ' (' + d.specialty + ')') for d in doctors]
    if form.validate_on_submit():
        doctor = Doctor.query.get(form.doctor_id.data)
        appt = Appointment(
            patient_id=current_user.id,
            doctor_id=form.doctor_id.data,
            date_time=form.date_time.data,
            reason=form.reason.data,
            fee=doctor.consultation_fee,
            status='pending'
        )
        if is_available(form.doctor_id.data, form.date_time.data):
            db.session.add(appt)
            db.session.commit()
            flash('Appointment booked successfully!')
            return redirect(url_for('patient.dashboard'))
        flash('Slot not available')
    return render_template('patient/book.html', form=form)

@bp.route('/cancel/<int:appt_id>')
@login_required
@role_required('patient')
def cancel(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    if appt.patient_id == current_user.id and appt.status == 'pending':
        appt.status = 'cancelled'
        db.session.commit()
        flash('Appointment cancelled')
    return redirect(url_for('patient.dashboard'))

