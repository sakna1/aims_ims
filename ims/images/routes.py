from flask import Blueprint, render_template, session, flash, redirect, url_for,request,send_from_directory
from ims.images.service import ImageService
from ims.patients.service import PatientService
from ims.patients.routes import patient_required
from ims.staff.routes import staff_required

images_bp = Blueprint("images_bp", __name__)


@images_bp.route("/upload-images", methods=["GET", "POST"])
@staff_required
def upload_images():
    patients = PatientService.get_all_patients()
    categories = ImageService.get_all_categories()  # 🔥 NEW — load categories

    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        image_files = request.files.getlist("images")
        image_type = request.form.get("image_type")  # category_id
        description = request.form.get("description")

        uploaded_by = session.get("user_id")

        if not uploaded_by:
            flash("Please login first!", "danger")
            return redirect(url_for("auth_bp.login"))

        ImageService.upload_images(
            patient_id=patient_id,
            uploaded_by=uploaded_by,
            images=image_files,
            image_type=image_type,  # category id
            description=description
        )

        flash("Images uploaded successfully!", "success")
        return redirect(url_for("images_bp.upload_images"))

    return render_template(
        "radiologist/upload_image.html",
        patients=patients,
        categories=categories     
    )

@images_bp.route("/my-images")
@staff_required
def view_images_staff():
    staff_id = session.get("user_id")

    if not staff_id:
        flash("Please login first!", "danger")
        return redirect(url_for("auth_bp.login"))

    # Fetch images uploaded by logged-in radiologist/staff
    images = ImageService.get_uploaded_images(staff_id)

    return render_template("radiologist/view_images.html", images=images)

@images_bp.route("/select-image", methods=["GET"])
@staff_required
def select_image():
    images = ImageService.get_images_without_report()
    return render_template("radiologist/select_image.html", images=images)

@images_bp.route("/view/<filename>")
def view_file(filename):
    if not session.get("user_id") and not session.get("patient_id"):
        flash("Please login first!", "danger")
        return redirect(url_for("auth_bp.login"))

    folder = r"D:\sakna\Sakna Perera\Lec\Software Architecture and Programming\CW2\AIMS\abc_ims\uploads"
    return send_from_directory(folder, filename)

@images_bp.route("/delete/<int:id>", methods=["POST"])
@staff_required
def delete_image(id):
    success = ImageService.delete_image(id)

    if success:
        flash("Image deleted successfully!", "success")
    else:
        flash("Image not found!", "danger")

    return redirect(url_for("images_bp.view_images_staff"))


