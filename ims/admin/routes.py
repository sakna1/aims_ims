# ims/admin/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from ims.admin.service import AdminService
from ims.patients.service import PatientService
from ims.staff.service import StaffService 

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    url_prefix="/admin",
    template_folder="templates"
)

def admin_required(f):
    
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@admin_bp.route("/dashboard")
def dashboard():
    # Check if user is logged in and is admin
    if "role" not in session or session["role"] != "admin":
        flash("Access denied", "danger")
        return redirect(url_for("auth_bp.login"))

    # Fetch counts from service
    total_patients = AdminService.count_patients()
    total_staff = AdminService.count_staff()
    total_categories = AdminService.count_categories()

    return render_template(
        "admin/dashboard.html",
        total_patients=total_patients,
        total_staff=total_staff,
        total_categories= total_categories
    )

@admin_bp.route('/patients')
@admin_required
def patients_page():   
    patients = PatientService.list_patients()
    return render_template('admin/patients.html', patients=patients)

@admin_bp.route('/staff')
@admin_required
def staff_page():
    staff_list = StaffService.list_staff()
    return render_template('admin/staff.html', staff=staff_list)

@admin_bp.route('/categories')
@admin_required
def categories_page():
    categories = AdminService.list_categories()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route("/staff/add", methods=["GET", "POST"])
@admin_required
def add_staff():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        role = request.form.get("role")

        # Required validation
        if not username or not password or not full_name or not role:
            flash("Please fill required fields", "danger")
            return render_template("admin/staff_form.html")

        # Create staff
        StaffService.create_staff(
            username=username,
            password=password,
            full_name=full_name,
            email=email,
            role=role
        )

        flash("Staff created", "success")
        return redirect(url_for("admin_bp.dashboard"))

    return render_template("admin/staff_form.html")

@admin_bp.route("/patients/add", methods=["GET", "POST"])
@admin_required
def add_patient():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        address = request.form.get("address")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        conditions = request.form.get("conditions")

        if not first_name or not last_name:
            flash("Please provide patient name", "danger")
            return render_template("admin/patient_form.html")

        PatientService.create_patient(
            username,password,first_name, last_name, address, dob,
            gender, conditions
        )

        flash("Patient created", "success")
        return redirect(url_for("admin_bp.dashboard"))

    return render_template("admin/patient_form.html")

@admin_bp.route("/categories/add", methods=["GET", "POST"])
@admin_required
def add_category():
    if request.method == "POST":
        name = request.form.get("name")

        if not name:
            flash("Category name is required", "danger")
            return render_template("admin/category_form.html")

        AdminService.create_category(name)
        flash("Category added successfully", "success")
        return redirect(url_for("admin_bp.dashboard"))

    return render_template("admin/category_form.html", category=None)

@admin_bp.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
@admin_required
def edit_patient(patient_id):
    patient = PatientService.get_patient(patient_id)
    if request.method == 'POST':
        # Update patient with form data
        PatientService.update_patient(
            patient_id,
            password = request.form.get("password"),
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            address=request.form.get('address'),
            gender=request.form.get('gender'),
            conditions=request.form.get('conditions')
        )
        flash("Patient updated", "success")
        return redirect(url_for('admin_bp.patients_page'))

    return render_template('admin/patient_form.html', patient=patient)

@admin_bp.route('/patients/delete/<int:patient_id>', methods=['POST'])
@admin_required
def delete_patient(patient_id):
    success = PatientService.delete_patient(patient_id)
    if success:
        flash("Patient deleted", "success")
    else:
        flash("Patient not found", "warning")
    return redirect(url_for('admin_bp.patients_page'))

@admin_bp.route('/staff/edit/<int:staff_id>', methods=['GET', 'POST'])
@admin_required
def edit_staff(staff_id):
    staff = StaffService.get_staff_by_id(staff_id)

    if request.method == 'POST':
        StaffService.update_staff(
            staff_id,
            username=request.form.get('username'),
            full_name=request.form.get('full_name'),
            email=request.form.get('email'),
            role=request.form.get('role'),
            password=request.form.get('password')  # handled safely in service
        )

        flash("Staff updated successfully", "success")
        return redirect(url_for('admin_bp.staff_page'))

    return render_template('admin/staff_form.html', staff=staff)

@admin_bp.route('/staff/delete/<int:staff_id>', methods=['POST'])
@admin_required
def delete_staff(staff_id):
    success = StaffService.delete_staff(staff_id)

    if success:
        flash("Staff member deleted", "success")
    else:
        flash("Staff not found", "warning")

    return redirect(url_for('admin_bp.staff_page'))

@admin_bp.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@admin_required
def edit_category(category_id):
    category = AdminService.get_category(category_id)

    if request.method == 'POST':
        AdminService.update_category(
            category_id,
            name=request.form.get('name')
        )
        flash("Category updated", "success")
        return redirect(url_for('admin_bp.categories_page'))

    return render_template('admin/category_form.html', category=category)

@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@admin_required
def delete_category(category_id):
    success = AdminService.delete_category(category_id)

    if success:
        flash("Category deleted", "success")
    else:
        flash("Category not found", "warning")

    return redirect(url_for('admin_bp.categories_page'))
