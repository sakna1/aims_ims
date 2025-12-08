# ims/staff/routes.py
from flask import Blueprint, render_template
from ims.models import Patient, Image, Report  # adjust imports if needed

staff_bp = Blueprint(
    "staff_bp",
    __name__,
    url_prefix="/staff",
    template_folder="templates"
)

@staff_bp.route("/dashboard")
def radiologist_dashboard():
    
    return render_template(
        "radiologist/dashboard.html",
       
    )
