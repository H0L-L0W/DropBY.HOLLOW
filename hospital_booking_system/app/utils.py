from functools import wraps
from flask import abort
from flask_login import current_user
from app.models import Role, Appointment, Doctor

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def is_available(doctor_id, date_time):
    """Check if doctor slot is available"""
    appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.date_time == date_time,
        Appointment.status != 'cancelled'
    ).count()
    return appointments == 0

def calculate_revenue(start_date, end_date):
    from app.models import RevenueLog
    return RevenueLog.query.filter(
        RevenueLog.timestamp >= start_date,
        RevenueLog.timestamp <= end_date
    ).sum(RevenueLog.amount) or 0

# Email helpers
def send_email(to, subject, template, **kwargs):
    # Implement with Flask-Mail later
    pass

