from flask import Blueprint, render_template, session, flash, redirect, url_for
from ims.billing.service import BillingService
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

    billing_items = BillingService.get_billing_by_patient_id(patient_id)
    total_cost = BillingService.calculate_total_cost(patient_id)

    payment_status = "Pending" if total_cost > 0 else "Completed"

    return render_template(
        "patient/billing.html",
        billing_items=billing_items,
        total_cost=total_cost,
        payment_status=payment_status
    )
