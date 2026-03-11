from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), nullable=False)

    student = db.relationship('Student', back_populates='user', uselist=False)
    company = db.relationship('Company', back_populates='user', uselist=False)


class Student(db.Model):
    
    __tablename__ = "students"
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    ug_collage_name = db.Column(db.String(100), nullable=False)
    ug_degree = db.Column(db.String(50), nullable=False)
    ug_branch = db.Column(db.String(50), nullable=False)
    ug_graduation_year = db.Column(db.Integer, nullable=False)
    ug_cgpa = db.Column(db.Float, nullable=False)

    pg_collage_name = db.Column(db.String(100),nullable=True)
    pg_degree = db.Column(db.String(50),nullable=True)
    pg_branch = db.Column(db.String(50),nullable=True)
    pg_graduation_year = db.Column(db.Integer,nullable=True)
    pg_cgpa = db.Column(db.Float,nullable=True)
    resume = db.Column(db.String(200),nullable=True)

    user = db.relationship('User', back_populates='student')
    applications = db.relationship('Application', back_populates='student')  


class Company(db.Model):
    
    __tablename__ = "companies"
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    website = db.Column(db.String(200))
    hr_name = db.Column(db.String(100), nullable=False)
    hr_contact = db.Column(db.String(20), nullable=False)
    about_company = db.Column(db.String(500))

    user = db.relationship('User', back_populates='company')
    placement_drives = db.relationship('Placement_drive', back_populates='company') 


class Placement_drive(db.Model):
    
    __tablename__ = "placement_drive"
    
    drive_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    drive_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.String(200), nullable=False)
    application_deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False,  default="pending")

    company = db.relationship('Company', back_populates='placement_drives')     
    applications = db.relationship('Application', back_populates='placement_drive')  


class Application(db.Model):
    
    __tablename__ = "application"
    
    application_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    placement_drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.drive_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    student = db.relationship('Student', back_populates='applications') 
    placement_drive = db.relationship('Placement_drive', back_populates='applications')