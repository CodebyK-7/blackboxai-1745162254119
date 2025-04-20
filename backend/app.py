from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, Student, Company, Job, Application

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    academic_details = data.get('academic_details', '')
    personal_details = data.get('personal_details', '')

    if Student.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    password_hash = generate_password_hash(password)
    new_student = Student(email=email, password_hash=password_hash, full_name=full_name,
                          academic_details=academic_details, personal_details=personal_details)
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = Student.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/jobs', methods=['GET'])
@login_required
def get_jobs():
    jobs = Job.query.all()
    jobs_list = []
    for job in jobs:
        jobs_list.append({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'location': job.location,
            'company': job.company.name,
            'eligibility_criteria': job.eligibility_criteria
        })
    return jsonify(jobs_list)

@app.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    student = current_user

    # Simple eligibility check: check if student's academic details contain keywords from eligibility_criteria
    if job.eligibility_criteria:
        criteria_keywords = job.eligibility_criteria.lower().split()
        student_academic = (student.academic_details or '').lower()
        if not any(keyword in student_academic for keyword in criteria_keywords):
            return jsonify({'message': 'You are not eligible for this job'}), 403

    existing_application = Application.query.filter_by(student_id=student.id, job_id=job.id).first()
    if existing_application:
        return jsonify({'message': 'You have already applied for this job'}), 400

    application = Application(student_id=student.id, job_id=job.id)
    db.session.add(application)
    db.session.commit()
    return jsonify({'message': 'Application submitted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
