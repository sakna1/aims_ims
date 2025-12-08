from ims.models import Billing
from database.db import db
from sqlalchemy import func

class BillingService:

    @staticmethod
    def get_billing_by_patient_id(patient_id):
        return Billing.query.filter_by(patient_id=patient_id).all()

    @staticmethod
    def calculate_total_cost(patient_id):
        total = db.session.query(func.sum(Billing.cost_amount)) \
                          .filter(Billing.patient_id == patient_id) \
                          .scalar()
        return total if total else 0
