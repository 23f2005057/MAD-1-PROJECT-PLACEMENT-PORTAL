from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Student, Company, Placement_drive, Application
import datetime
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mad-1-project'


db.init_app(app)

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username="admin").first()

    if not admin:
        admin = User(
            username="admin",
            password="admin",
            role="admin",
            is_active=True,
            is_approved=True
        )

        db.session.add(admin)
        db.session.commit()
    


@app.route("/")
def start():
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

@app.route("/company_signup", methods=["GET", "POST"])
def company_signup():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        company_name = request.form.get("CompanyName")
        company_industry = request.form.get("industry")
        company_website = request.form.get("website")
        hr_name = request.form.get("hr_name")
        hr_number = request.form.get("hr_number")
        about = request.form.get("about")
        

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Username already exists"
        
        new_user = User(
            username=username,
            password=password,
            role="company",
            is_active=True,
            is_approved=False
        )

        db.session.add(new_user)
        db.session.flush()

        new_company=Company(
            id=new_user.id,
            
            name=company_name,
            industry = company_industry,
            website = company_website,
            hr_name = hr_name,
            hr_contact = hr_number,
            about_company = about
        )
        db.session.add(new_company)
        db.session.commit()
       
        return render_template("login.html")

    return render_template("company_signup.html")

@app.route("/student_signup", methods=["GET", "POST"])
def student_signup():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("Password")
        email = request.form.get("email")

        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        dob = request.form.get("dob")

        phone = request.form.get("phone")
        address = request.form.get("address")
        gender = request.form.get("gender")

        ug_collage_name = request.form.get("ug_collage_name")
        ug_degree = request.form.get("ug_degree")
        ug_branch = request.form.get("ug_branch")
        ug_graduation_year = request.form.get("ug_graduation_year")
        ug_cgpa = request.form.get("ug_cgpa")

        def to_float(pg_cgpa):
            if pg_cgpa == "" or pg_cgpa is None:
                return None
            return float(pg_cgpa)

        pg_collage_name = request.form.get("pg_collage_name")
        pg_degree = request.form.get("pg_degree")
        pg_branch = request.form.get("pg_branch")
        pg_graduation_year = request.form.get("pg_graduation_year")
        pg_cgpa = to_float(request.form.get("pg_cgpa"))
        


        resume = request.form.get("resume")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Username already exists"


        existing_email = Student.query.filter_by(email=email).first()

        if existing_email:
            return "Email already registered"


        new_user = User(
            username=username,
            password=password,
            role="student",
            is_active=True,
            is_approved=True
        )

        db.session.add(new_user)
        db.session.flush()
        

        new_student = Student(
            id=new_user.id,
            first_name=firstname,
            last_name=lastname,
            email=email,
            date_of_birth=datetime.datetime.strptime(dob, "%Y-%m-%d"),
            phone=phone,
            address=address,
            gender=gender,

            ug_collage_name=ug_collage_name,
            ug_degree=ug_degree,
            ug_branch=ug_branch,
            ug_graduation_year=ug_graduation_year,
            ug_cgpa=ug_cgpa,

            pg_collage_name=pg_collage_name,
            pg_degree=pg_degree,
            pg_branch=pg_branch,
            pg_graduation_year=pg_graduation_year,
            pg_cgpa=pg_cgpa,

            resume=resume
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("student_signup.html")
    
@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("Password")
        role = request.form.get("role")

        print(username," ",password," ",role)
        user = User.query.filter_by(username=username, password=password, role=role).first()

        if not user:
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))   

        if not user.is_active:
            flash("Account is blacklisted", "danger")
            return redirect(url_for("login"))
        
        if role == "company" and not user.is_approved:
            flash("Account not yet approved by admin", "warning")
            return redirect(url_for("login"))
        
        session["user_id"] = user.id
        session["role"] = user.role
        
        if role == "student":
            return redirect(url_for("student_dashboard"))

        if role == "company":
            if not user.is_approved:
                return "Account not approved by admin"
            return redirect(url_for("company_dashboard"))

        if role == "admin":
            return redirect(url_for("admin_dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return "Unauthorized access"
    
    search = request.args.get('search', '')
    
    if search:
        students = Student.query.filter(
            or_(
                Student.first_name.contains(search),
                Student.last_name.contains(search),
                Student.email.contains(search)
            )
        ).all()

        companies = Company.query.filter(
            or_(
                Company.name.contains(search),
                Company.industry.contains(search)
            )
        ).all()

        if search.isdigit():                                          
            student_by_id = Student.query.get(int(search))          
            if student_by_id and student_by_id not in students:     
             students.append(student_by_id)                      

            company_by_id = Company.query.get(int(search))          
            if company_by_id and company_by_id not in companies:    
                companies.append(company_by_id)
    else:
        students = Student.query.all()
        companies = Company.query.all()


    user=User.query.all()
    drives=Placement_drive.query.all()
    applications=Application.query.all()
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Placement_drive.query.count()
    total_applications = Application.query.count()
    return render_template("admin_dashboard.html",
                           user=user,
                           students=students,
                           companies=companies,
                           drives=drives,
                           applications=applications,
                           total_students=total_students,
                           total_companies=total_companies,
                           total_drives=total_drives,
                           total_applications=total_applications,
                           search=search
                           )    

@app.route("/admin/blacklist_user/<int:id>",methods=["POST"])
def blacklist_user(id):
    if session.get("role") != "admin":
        return "Unauthorized access"
    
    user = User.query.get(id)

    if not user:
        return "User not found"

    user.is_active = False
    db.session.commit()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete_student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    if session.get("role") != "admin":
        return "Unauthorized access"
    student = Student.query.get(student_id)
    if not student:
        return "Student not found"
    Application.query.filter_by(student_id=student_id).delete()
    user = User.query.get(student_id)
    db.session.delete(student)
    if user:
        db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete_company/<int:company_id>", methods=["POST"])
def delete_company(company_id):
    if session.get("role") != "admin":
        return "Unauthorized access"
    company = Company.query.get(company_id)
    if not company:
        return "Company not found"
    for drive in company.placement_drives:
        Application.query.filter_by(placement_drive_id=drive.drive_id).delete()
        db.session.delete(drive)
    user = User.query.get(company_id)
    db.session.delete(company)
    if user:
        db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/unblacklist_user/<int:id>",methods=["POST"])
def unblacklist_user(id):
    if session.get("role") != "admin":
        return "Unauthorized access"
    
    user = User.query.get(id)

    if not user:
        return "User not found"

    user.is_active = True
    db.session.commit()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/approve_company/<int:user_id>", methods=["POST"])
def approve_company(user_id):
    if session.get("role") != "admin":
        return "Unauthorized access"
    user = User.query.get(user_id)

    if not user:
        return "User not found"

    user.is_approved = True
    db.session.commit()

    return redirect(url_for("admin_dashboard"))

@app.route("/company_dashboard")
def company_dashboard():
    if session.get("role") != "company":
        return "Unauthorized access"
    
    company=Company.query.filter_by(id=session.get("user_id")).first()
    pending_drives=[drive for drive in company.placement_drives if drive.status == "pending"]
    ongoing_drives=[drive for drive in company.placement_drives if drive.status == "active"]
    closer_drives=[drive for drive in company.placement_drives if drive.status == "closed"]
    show_form = request.args.get("show_form", False)
    show_update = request.args.get("show_update", False)

    return render_template("company_dashboard.html",
                           company=company,
                           ongoing_drives=ongoing_drives,
                           closed_drives=closer_drives,
                           pending_drives=pending_drives,  
                           show_form=show_form,
                           show_update=show_update                       
                           )

@app.route("/company_dashboard/edit_profile", methods=["GET", "POST"])
def company_edit_profile():
    if session.get("role") != "company":
        return "Unauthorized access"
    
    company = Company.query.get(session.get("user_id"))
    user = User.query.get(session.get("user_id"))

    if request.method == "POST":
        password = request.form.get("password")
        name = request.form.get("name")
        industry = request.form.get("industry")
        website = request.form.get("website")
        hr_name = request.form.get("hr_name")
        hr_contact = request.form.get("hr_contact")
        about = request.form.get("about")

        if password: user.password = password
        if name: company.name = name
        if industry: company.industry = industry
        if website: company.website = website
        if hr_name: company.hr_name = hr_name
        if hr_contact: company.hr_contact = hr_contact
        if about: company.about_company = about

        db.session.commit()
        return redirect(url_for("company_dashboard"))

    return render_template("company_edit_profile.html", company=company)


@app.route("/company_dashboard/create_drive", methods=["POST"])
def create_drive():
    if session.get("role") != "company":
        return "Unauthorized access"
    
    company = Company.query.filter_by(id=session.get("user_id")).first()

    if not company:
        return "Company not found"

    drive_name = request.form.get("drive_name")
    description = request.form.get("description")
    job_title = request.form.get("job_title")
    eligibility = request.form.get("eligibility")
    application_deadline = request.form.get("Deadline")

    new_drive = Placement_drive(
        company_id=company.id,
        drive_name=drive_name,
        description=description,
        eligibility=eligibility,
        application_deadline=datetime.date.fromisoformat(application_deadline),
        job_title=job_title,
        status="pending"
    )

    db.session.add(new_drive)
    db.session.commit()

    return redirect(url_for("company_dashboard"))

@app.route("/company_dashboard/update_drive/<int:drive_id>", methods=["POST"])
def update_drive(drive_id):
    if session.get("role") != "company":
        return "Unauthorized access"
    
    drive = Placement_drive.query.get(drive_id)

    if not drive:
        return "Drive not found"

    if drive.company_id != session.get("user_id"):
        return "Unauthorized access"

    drive_name = request.form.get("drive_name")
    description = request.form.get("description")
    job_title = request.form.get("job_title")
    eligibility = request.form.get("eligibility")
    application_deadline = request.form.get("Deadline")

    if drive_name:
        drive.drive_name = drive_name
    if description:
        drive.description = description
    if job_title:
        drive.job_title = job_title
    if eligibility:
        drive.eligibility = eligibility
    if application_deadline:
        drive.application_deadline = datetime.date.fromisoformat(application_deadline)

    db.session.commit()

    return redirect(url_for("company_dashboard"))

@app.route("/company_dashboard/delete_drive/<int:drive_id>",methods=["POST"])
def delete_drive(drive_id):
    if session.get("role") != "company":
        return "Unauthorized access"
    
    drive = Placement_drive.query.get(drive_id)

    if not drive:
        return "Drive not found"

    if drive.company_id != session.get("user_id"):
        return "Unauthorized access"

    db.session.delete(drive)
    db.session.commit()

    return redirect(url_for("company_dashboard"))

@app.route("/company_dashboard/close_drive/<int:drive_id>", methods=["POST"])
def close_drive(drive_id):
    if session.get("role") != "company":
        return "Unauthorized access"
    
    drive = Placement_drive.query.get(drive_id)

    if not drive:
        return "Drive not found"

    if drive.company_id != session.get("user_id"):
        return "Unauthorized access"

    drive.status = "closed"
    db.session.commit()

    return redirect(url_for("company_dashboard"))

@app.route("/admin_dashboard/activate_drive/<int:drive_id>", methods=["POST"])
def activate_drive(drive_id):
    if session.get("role") != "admin":
        return "Unauthorized access"
    
    drive = Placement_drive.query.get(drive_id)

    if not drive:
        return "Drive not found"

    drive.status = "active"
    db.session.commit()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin_dashboard/reject_drive/<int:drive_id>", methods=["POST"])
def reject_drive(drive_id):
    if session.get("role") != "admin":
        return "Unauthorized access"
    
    drive = Placement_drive.query.get(drive_id)

    if not drive:
        return "Drive not found"

    db.session.delete(drive)
    db.session.commit()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin_dashboard/view_drive/<int:drive_id>",methods=["GET"])
def view_drive(drive_id):
    if session.get("role") != "admin":
        return "Unauthorized access"
    
    drive = Placement_drive.query.get(drive_id)

    if not drive:
        return "Drive not found"
    
    return render_template("view_drive.html", drive=drive)

@app.route("/company_dashboard/view_drive/<int:drive_id>",methods=["GET"])
def view_drive_company(drive_id):
    if session.get("role") != "company":
        return "Unauthorized access"
    
    drive = Placement_drive.query.get(drive_id)

    if not drive:
        return "Drive not found"
    
    if drive.company_id != session.get("user_id"):
        return "Unauthorized access"
    
    return render_template("view_drive.html", drive=drive)

@app.route("/company_dashboard/view_applications/<int:drive_id>", methods=["GET"])
def view_applications(drive_id):
    if session.get("role") != "company":
        return "Unauthorized access"
    drive = Placement_drive.query.get(drive_id)
    if not drive:
        return "Drive not found"
    if drive.company_id != session.get("user_id"):
        return "Unauthorized access"
    return render_template("view_application.html", drive=drive, applications=drive.applications)

@app.route("/company_dashboard/review_application/<int:application_id>", methods=["GET", "POST"])
def review_application(application_id):
    if session.get("role") != "company":
        return "Unauthorized access"
    
    application = Application.query.get(application_id)

    if not application:
        return "Application not found"

    if application.placement_drive.company_id != session.get("user_id"):
        return "Unauthorized access"

    if request.method == "POST":
        status = request.form.get("status")
        application.status = status
        db.session.commit()
        return redirect(url_for("view_applications", drive_id=application.placement_drive_id))

    return render_template("review_application.html", application=application)

@app.route("/student_dashboard", methods=["GET"])
def student_dashboard():
    if session.get("role") != "student":
        return "Unauthorized access"
    
    student=Student.query.filter_by(id=session.get("user_id")).first()
    approved_companies = Company.query.join(User).filter(User.is_approved == True, User.is_active==True).all()
    applied_drives=Application.query.filter_by(student_id=student.id).all()
    current_applications = [a for a in applied_drives if a.status in ["applied", "shortlisted"]][:5]
    past_applications = [a for a in applied_drives if a.status in ["selected", "rejected"]][:5]

    return render_template("student_dashboard.html", 
                           student=student,
                           company=approved_companies,
                           apllication=applied_drives,
                           current_applications=current_applications,
                           past_applications=past_applications
                           )

@app.route("/student_dashboard/view_company/<int:id>")
def view_company(id):
    if session.get("role") != "student":
        return "Unauthorized access"
    
    company=Company.query.filter_by(id=id).first()
    ongoing_drives=Placement_drive.query.filter_by(company_id=id, status="active").all()
    return render_template("view_company.html", 
                           company=company,
                           ongoing_drives=ongoing_drives)

@app.route("/student_dashboard/student_view_drive/<int:drive_id>",methods=["GET","POST"])
def student_view_drive(drive_id):
    if session.get("role") != "student":
        return "Unauthorized access"
    
    drive = Placement_drive.query.get(drive_id)

    if not drive:
        return "Drive not found"
    
    already_applied = Application.query.filter_by(
                    student_id=session.get("user_id"),
                        placement_drive_id=drive_id).first()
    return render_template("student_view_drive.html", drive=drive, already_applied=already_applied)

@app.route("/student_dashboard/apply/<int:drive_id>", methods=["POST"])
def apply_drive(drive_id):
    if session.get("role") != "student":
        return "Unauthorized access"
    
    existing = Application.query.filter_by(
        student_id=session.get("user_id"),
        placement_drive_id=drive_id
    ).first()

    if existing:
        return "Already applied"

    new_application = Application(
        student_id=session.get("user_id"),
        placement_drive_id=drive_id,
        status="applied"
    )
    db.session.add(new_application)
    db.session.commit()

    return redirect(url_for("student_dashboard"))

@app.route("/student_dashboard/history")
def history():
    if session.get("role") != "student":
        return "Unauthorized access"
    
    student = Student.query.get(session.get("user_id"))
    past_applications = Application.query.filter_by(student_id=student.id).all()

    return render_template("student_history.html",
                           student=student,
                           past_applications=past_applications)

@app.route("/student_dashboard/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if session.get("role") != "student":
        return "Unauthorized access"
    
    student = Student.query.get(session.get("user_id"))
    user = User.query.get(session.get("user_id"))

    if request.method == "POST":
        
        password = request.form.get("Password")
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        dob = request.form.get("dob")
        phone = request.form.get("phone")
        address = request.form.get("address")
        gender = request.form.get("gender")
        ug_collage_name = request.form.get("ug_collage_name")
        ug_degree = request.form.get("ug_degree")
        ug_branch = request.form.get("ug_branch")
        ug_graduation_year = request.form.get("ug_graduation_year")
        ug_cgpa = request.form.get("ug_cgpa")
        pg_collage_name = request.form.get("pg_collage_name")
        pg_degree = request.form.get("pg_degree")
        pg_branch = request.form.get("pg_branch")
        pg_graduation_year = request.form.get("pg_graduation_year")
        pg_cgpa = request.form.get("pg_cgpa")
        resume = request.form.get("resume")
        
        if password: user.password = password
        if email: student.email = email
        if firstname: student.first_name = firstname
        if lastname: student.last_name = lastname
        if dob: student.date_of_birth = datetime.date.fromisoformat(dob)
        if phone: student.phone = phone
        if address: student.address = address
        if gender: student.gender = gender
        if ug_collage_name: student.ug_collage_name = ug_collage_name
        if ug_degree: student.ug_degree = ug_degree
        if ug_branch: student.ug_branch = ug_branch
        if ug_graduation_year: student.ug_graduation_year = ug_graduation_year
        if ug_cgpa: student.ug_cgpa = ug_cgpa
        if pg_collage_name: student.pg_collage_name = pg_collage_name
        if pg_degree: student.pg_degree = pg_degree
        if pg_branch: student.pg_branch = pg_branch
        if pg_graduation_year: student.pg_graduation_year = pg_graduation_year
        if pg_cgpa: student.pg_cgpa = pg_cgpa
        if resume: student.resume = resume

        db.session.commit()
        return redirect(url_for("student_dashboard"))

    return render_template("student_profile_edit.html", student=student)

@app.route("/admin/view_application/<int:application_id>")
def admin_view_application(application_id):
    if session.get("role") != "admin":
        return "Unauthorized access"
    application = Application.query.get(application_id)
    if not application:
        return "Application not found"
    return render_template("admin_view_application.html", application=application)






