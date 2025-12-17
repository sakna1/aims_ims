# ims/staff/routes.py
from flask import Blueprint, render_template,request,redirect, url_for, flash, session
from ims.models import Patient, Image, Report  # adjust imports if needed
from ims.staff.service import StaffService 
from ims.images.service import ImageService
from ims.patients.service import PatientService
from ims.admin.service import AdminService

staff_bp = Blueprint(
    "staff_bp",
    __name__,
    url_prefix="/staff",
    template_folder="templates"
)
def staff_required(f):
    def wrapper(*args, **kwargs):
        allowed_roles = ["radiologist", "doctor", "finance"]  

        if "role" not in session or session["role"] not in allowed_roles:
            flash("Access denied", "danger")
            return redirect(url_for("auth_bp.login"))

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


# Radiologist Dashboard
@staff_bp.route("/radiologist/dashboard")
@staff_required
def radiologist_dashboard():     
    total_patients = AdminService.total_patients_count()
    total_images = ImageService.get_all_images_count()
    total_reports = StaffService.get_all_reports()
    return render_template("radiologist/dashboard.html",total_patients=total_patients,
        total_images=total_images,
        total_reports=total_reports)


# Doctor Dashboard
@staff_bp.route("/doctor/dashboard")
@staff_required
def doctor_dashboard():
    return render_template("doctor/dashboard.html")

# finance Dashboard
@staff_bp.route("/finance/dashboard")
@staff_required
def finance_dashboard():
    return render_template("finance/dashboard.html")


# radiologist routes

@staff_bp.route("/create-report/<int:image_id>", methods=["GET", "POST"])
def create_report(image_id):
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login first!", "danger")
        return redirect(url_for("auth_bp.login"))

    image = StaffService.get_image(image_id)
    report = StaffService.get_report_by_image(image_id)

    if not image:
        flash("Image not found!", "danger")
        return redirect(url_for("staff_bp.view_reports"))

    if request.method == "POST":
        report_text = request.form.get("report_text")
        diagnosis = request.form.get("diagnosis")

        StaffService.save_report(
            patient_id=image.patient_id,
            image_id=image_id,
            created_by=user_id,
            report_text=report_text,
            diagnosis=diagnosis
        )

        flash("Report saved successfully!", "success")
        return redirect(url_for("staff_bp.view_reports"))

    return render_template(
        "radiologist/create_report.html",
        image=image,
        report=report
    )

@staff_bp.route("/view_reports")
def view_reports():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login first!", "danger")
        return redirect(url_for("auth_bp.login"))

    reports = StaffService.get_reports_by_radiologist(user_id)

    return render_template(
        "radiologist/view_reports.html",
        reports=reports
    )

# doctor routes

@staff_bp.route("/profile", methods=["GET"])
@staff_required
def profile():
    q = request.args.get("q")
    pid = request.args.get("id")

    # if patient ID passed → show profile
    if pid:
        patient = PatientService.get_patient_by_id(pid)
        if not patient:
            flash("Patient not found", "danger")
            return redirect(url_for('staff_bp.profile'))

        return render_template("doctor/profile.html", patient=patient)

    # if search query passed
    if q:
        patients = PatientService.search_patients(q)

        if len(patients) == 0:
            return render_template("doctor/profile_search.html",
                                   message="No patients found.")

        return render_template("doctor/profile_search.html",
                               patients=patients)

    # initial page
    return render_template("doctor/profile_search.html")

@staff_bp.route("/view-images", methods=["GET"])
def view_images():
    query = request.args.get("query")

    patient = None
    images = []

    if query:
        # Search patient by ID or name
        patient = PatientService.find_by_id_or_name(query)

        if patient:
            images = ImageService.get_images_by_patient_id(patient.id)

    return render_template(
        "doctor/images.html",
        patient=patient,
        images=images
    )

@staff_bp.route("/reports", methods=["GET"])
def doctor_view_reports():
    query = request.args.get("query")
    patient = None
    reports = []

    if query:
        patient = PatientService.find_by_id_or_name(query)
        if patient:
            reports = StaffService.get_reports_by_patient(patient.id)

    return render_template(
        "doctor/reports.html",
        patient=patient,
        reports=reports
    )

@staff_bp.route("/update-report/<int:report_id>", methods=["POST"])
def doctor_update_report(report_id):
    disease_type = request.form.get("disease_type")
    diagnosis = request.form.get("diagnosis")
    status = request.form.get("status")

    StaffService.update_report(report_id, disease_type, diagnosis, status)
    flash("Report updated successfully!", "success")

    return redirect(request.referrer)



