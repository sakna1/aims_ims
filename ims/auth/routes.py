# ims/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ims.auth.service import AuthService

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

            # Ensure role exists
            role = user.role.lower()
            session["role"] = role

            # Redirect based on role
            if role in ["admin", "staff"]:
                return redirect(url_for("admin_bp.dashboard"))

            elif role == "doctor":
                return redirect(url_for("doctor_bp.dashboard"))

            elif role == "radiologist":
                return redirect(url_for("radiologist_bp.dashboard"))

            elif role == "patient":
                return redirect(url_for("patient_bp.dashboard"))

            else:
                flash("Unknown user role", "danger")
                return redirect(url_for("auth_bp.login"))

        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

