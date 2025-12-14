from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from ims.billing.service import BillingService
from ims.images.service import ImageService

from ims.patients.routes import patient_required  # reuse decorator

billing_bp = Blueprint(
    "billing_bp",
    __name__,
    url_prefix="/billing"
)

@billing_bp.route("/")
@patient_required
def billing_patient():

    patient_id = session.get("patient_id")

    billing_items = BillingService.get_billing_by_patient(patient_id)
    total_cost = BillingService.calculate_total_cost(patient_id)

    payment_status = "Pending" if total_cost > 0 else "Completed"

    return render_template(
        "patient/billing.html",
        billing_items=billing_items,
        total_cost=total_cost,
        payment_status=payment_status
    )

@billing_bp.route("/add-billing", methods=["GET", "POST"])
def add_billing():
    categories = ImageService.get_all_categories()
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        task_name = request.form["task_name"]
        cost_amount = request.form["cost_amount"]

        BillingService.add_billing(patient_id, task_name, cost_amount)

        flash("Billing record added!", "success")
        return redirect(url_for("staff_bp.finance_dashboard"))

    return render_template("finance/add_billing.html" ,categories=categories)

@billing_bp.route("/search", methods=["GET", "POST"])
def search_patient():
    records = None
    total = 0
    patient_id = None

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        records = BillingService.get_billing_by_patient(patient_id)
        total = BillingService.get_total_for_patient(patient_id)

        return render_template(
            "finance/patient_billing.html",
            patient_id=patient_id,
            records=records,
            total=total
        )

    return render_template("finance/search_patient.html")

@billing_bp.route("/patients")
def view_patients():
    patients = BillingService.get_all_patients_summary()
    return render_template("finance/all_patients.html", patients=patients)

@billing_bp.route("/patient/<int:patient_id>")
def view_patient_billing(patient_id):
    records = BillingService.get_billing_by_patient(patient_id)
    total = BillingService.get_total_for_patient(patient_id)

    return render_template(
        "finance/patient_billing.html",
        patient_id=patient_id,
        records=records,
        total=total
    )

@billing_bp.route("/invoice/<int:patient_id>")
def generate_invoice(patient_id):
    records = BillingService.get_billing_by_patient(patient_id)
    total = BillingService.get_total_for_patient(patient_id)

    return render_template(
        "finance/invoice.html",
        patient_id=patient_id,
        records=records,
        total=total
    )


