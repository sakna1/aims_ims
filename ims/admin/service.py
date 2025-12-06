# ims/admin/service.py
from database.db import db
from ims.models.user import User
from ims.models.patient import Patient
from ims.models.billing import Billing
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask import session


class AdminService:

    # -------------------------
    # STAFF MANAGEMENT
    # -------------------------

    @staticmethod
    def create_staff(username, password, full_name, email, role):
        try:
            user = User(
                username=username,
                full_name=full_name,
                email=email,
                role=role
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()
            return user

        except SQLAlchemyError:
            db.session.rollback()
            return None

    @staticmethod
    def update_staff(user_id, **kwargs):
        staff = User.query.get(user_id)
        if not staff:
            return None

        for field, value in kwargs.items():
            if hasattr(staff, field) and value is not None:
                setattr(staff, field, value)

        try:
            db.session.commit()
            return staff
        except:
            db.session.rollback()
            return None


    @staticmethod
    def delete_staff(user_id):
        staff = User.query.get(user_id)
        if not staff:
            return False
        try:
            db.session.delete(staff)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def list_staff():
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def get_staff_by_id(user_id):
        return User.query.get(user_id)

    # -------------------------
    # PATIENT MANAGEMENT
    # -------------------------

    def create_patient(username,first_name, last_name, address=None, dob=None,
                       gender=None, conditions=None):

        try:
            # Convert dob string to date object
            dob_value = None
            if dob:
                dob_value = datetime.strptime(dob, "%Y-%m-%d").date()

            patient = Patient(
                username=username,
                first_name=first_name,
                last_name=last_name,
                address=address,
                dob=dob_value,
                gender=gender,
                conditions=conditions,
                created_by=session.get("user_id")  # logged-in user
            )

            db.session.add(patient)
            db.session.commit()
            return patient

        except SQLAlchemyError:
            db.session.rollback()
            return None

    @staticmethod
    def update_patient(patient_id, **kwargs):
        patient = Patient.query.get(patient_id)
        if not patient:
            return None
        for field, value in kwargs.items():
            if hasattr(patient, field) and value is not None:
                setattr(patient, field, value)
        try:
            db.session.commit()
            return patient
        except SQLAlchemyError:
            db.session.rollback()
            return None

    @staticmethod
    def delete_patient(patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            return False
        try:
            db.session.delete(patient)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def list_patients():
        return Patient.query.order_by(Patient.registration_date.desc()).all()

    @staticmethod
    def get_patient(patient_id):
        return Patient.query.get(patient_id)

    # -------------------------
    # DASHBOARD METRICS
    # -------------------------

    @staticmethod
    def total_patients_count():
        return db.session.query(db.func.count(Patient.id)).scalar() or 0

    @staticmethod
    def total_billing_amount():
        total = db.session.query(
            db.func.coalesce(db.func.sum(Billing.cost_amount), 0)
        ).scalar()
        return float(total or 0.0)
