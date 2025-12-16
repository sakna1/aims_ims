# ims/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ims.auth.service import AuthService
from ims.models.patient import Patient

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = AuthService.authenticate(username, password)
        
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            role = user.role.lower()
            session["role"] = role
            
            if role in ["admin", "staff"]:
                return redirect(url_for("admin_bp.dashboard"))

            elif role == "doctor":
                return redirect(url_for("staff_bp.doctor_dashboard"))

            elif role == "radiologist":
                return redirect(url_for("staff_bp.radiologist_dashboard"))
            
            elif role == "finance":
                return redirect(url_for("staff_bp.finance_dashboard"))

            elif role == "patient":
                patient = Patient.query.filter_by(username=username).first()
                if patient:
                    session["patient_id"] = patient.id
                    return redirect(url_for("patient_bp.dashboard"))
                else:
                    return render_template("login.html", error=True)

            else:
                return render_template("login.html", error=True)

        else:
            # ✅ THIS TRIGGERS POPUP
            return render_template("login.html", error=True)

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    AuthService.logout()
    return redirect(url_for("auth_bp.login"))

