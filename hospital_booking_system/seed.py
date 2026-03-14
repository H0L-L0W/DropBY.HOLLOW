from app import create_app, db
from app.models import User, Doctor, Department, Role

app = create_app()

with app.app_context():
    db.create_all()
    
    # Create dept
    dept = Department(name='General Medicine')
    db.session.add(dept)
    db.session.flush()
    
    # Admin
    admin = User(email='admin@hospital.com', first_name='Admin', last_name='User', role=Role.ADMIN)
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Doctor
    doctor = User(email='doctor@test.com', first_name='Dr John', last_name='Doe', role=Role.DOCTOR)
    doctor.set_password('doctor123')
    db.session.add(doctor)
    db.session.flush()
    d_profile = Doctor(user_id=doctor.id, department_id=dept.id, specialty='General Physician', consultation_fee=100.0)
    db.session.add(d_profile)
    
    db.session.commit()
    print('Seed complete: admin/admin123, doctor/doctor123')
