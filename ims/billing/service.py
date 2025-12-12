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
    
    @staticmethod
    def add_billing(patient_id, task_name, cost_amount):
        new_record = Billing(
            patient_id=patient_id,
            task_name=task_name,
            cost_amount=cost_amount
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record

    @staticmethod
    def get_billing_by_patient(patient_id):
        return Billing.query.filter_by(patient_id=patient_id).all()

    @staticmethod
    def get_total_for_patient(patient_id):
        total = db.session.query(func.sum(Billing.cost_amount))\
                    .filter(Billing.patient_id == patient_id)\
                    .scalar()
        return total or 0

    @staticmethod
    def get_all_patients_summary():
        results = db.session.query(
            Billing.patient_id.label("id"),
            func.sum(Billing.cost_amount).label("total_cost")
        ).group_by(Billing.patient_id).all()

        return results
