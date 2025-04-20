from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Student(UserMixin, db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    academic_details = db.Column(db.Text, nullable=True)
    personal_details = db.Column(db.Text, nullable=True)
    applications = db.relationship('Application', backref='student', lazy=True)

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    jobs = db.relationship('Job', backref='company', lazy=True)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    eligibility_criteria = db.Column(db.Text, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    applications = db.relationship('Application', backref='job', lazy=True)

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')
