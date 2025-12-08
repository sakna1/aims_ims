from flask import Blueprint, render_template, session, flash, redirect, url_for
from ims.images.service import ImageService
from ims.patients.routes import patient_required

images_bp = Blueprint(
    "images_bp",
    __name__,
    url_prefix="/images"
)

@images_bp.route("/")
@patient_required
def view_images():

    patient_id = session.get("patient_id")

    if not patient_id:
        flash("Patient session missing!", "danger")
        return redirect(url_for("patient_bp.dashboard"))

    images = ImageService.get_images_by_patient_id(patient_id)

    return render_template("patient/images.html", images=images)
