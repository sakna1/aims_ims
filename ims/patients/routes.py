# ims/patient/routes.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from ims.models import Patient
  
from ims.admin.service import AdminService

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
    return render_template("patient/dashboard.html")

@patient_bp.route("/profile")
@patient_required
def profile():
    return render_template("patient/profile.html")

@patient_bp.route("/view_images")
@patient_required
def view_images():    
    return render_template("patient/images.html")

@patient_bp.route("/billing")
@patient_required
def billing():
    return render_template("patient/billing.html")


@patient_bp.route("/view_reports")
@patient_required
def view_reports():
    return render_template("patient/reports.html")

