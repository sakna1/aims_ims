# ims/staff/routes.py
from flask import Blueprint, render_template,request,redirect, url_for, flash, session
from ims.models import Patient, Image, Report  # adjust imports if needed
from ims.staff.service import StaffService

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


@staff_bp.route("/dashboard")
@staff_required
def radiologist_dashboard():
    
    return render_template(
        "radiologist/dashboard.html",
       
    )

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




