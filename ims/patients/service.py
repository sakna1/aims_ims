from ims.models import Patient,Report
from database.db import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask import session
from sqlalchemy import or_
from ims.utils.security import hash_password
from ims.utils.helpers import parse_date

class PatientService:

    @staticmethod
    def get_patient_by_id(patient_id):
        return Patient.query.get(patient_id)

    @staticmethod
    def get_patient_by_user_id(user_id):
        return Patient.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def get_reports_by_patient_id(patient_id):
        return Report.query.filter_by(patient_id=patient_id)\
                           .order_by(Report.created_at.desc())\
                           .all()

    @staticmethod
    def get_report_by_id(report_id):
        return Report.query.get(report_id)
    

    #admin
    @staticmethod
    def create_patient(username,password,first_name, last_name, address=None, dob=None,
                       gender=None, conditions=None):

        try:
            # Convert dob string to date object
            dob_value = parse_date(dob)

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

            patient.password_hash = hash_password(password)

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

    #staff

    @staticmethod
    def get_patient(patient_id):
        return Patient.query.get(patient_id)
    
    @staticmethod
    def search_patients(query):
        if query.isdigit():
            return Patient.query.filter(Patient.id == int(query)).all()

        return Patient.query.filter(
            or_(
                Patient.first_name.ilike(f"%{query}%"),
                Patient.last_name.ilike(f"%{query}%")
            )
        ).all()

    @staticmethod
    def get_patient_by_id(pid):
        return Patient.query.filter_by(id=pid).first()
    
    @staticmethod
    def find_by_id_or_name(query):
    # Search by ID
        if query.isdigit():
            return Patient.query.filter_by(id=int(query)).first()

        # Search by first name OR last name
        return Patient.query.filter(
            or_(
                Patient.first_name.ilike(f"%{query}%"),
                Patient.last_name.ilike(f"%{query}%")
            )
        ).first()
    
    @staticmethod
    def get_all_patients():
        return Patient.query.all()

 