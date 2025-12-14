# ims/patient/routes.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from ims.models import Patient  
from ims.patients.service import PatientService
from ims.images.service import ImageService  

patient_bp = Blueprint(
    "patient_bp",
    __name__,
    url_prefix="/patient",
    template_folder="templates"
)

def patient_required(f):
    def wrapper(*args, **kwargs):
        if "role" not in session or session["role"] != "patient":
            flash("Access denied", "danger")
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@patient_bp.route("/dashboard")
@patient_required
def dashboard():
    patient_id = session.get("patient_id")
    patient = PatientService.get_patient_by_id(patient_id)

    return render_template("patient/dashboard.html", patient=patient)

@patient_bp.route("/profile")
@patient_required
def profile():
    patient_id = session.get("patient_id")
    patient = PatientService.get_patient_by_id(patient_id)

    if not patient:
        flash("Patient details not found!", "danger")
        return redirect(url_for("patient_bp.dashboard"))

    return render_template("patient/profile.html", patient=patient)

@patient_bp.route("/reports")
@patient_required
def view_reports():
    patient_id = session.get("patient_id")
    if not patient_id:
        flash("Patient session missing!", "danger")
        return redirect(url_for("patient_bp.dashboard"))

    reports = PatientService.get_reports_by_patient_id(patient_id)
    return render_template(
        "patient/reports.html",
        reports=reports
    )

