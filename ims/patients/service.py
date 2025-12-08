from ims.models import Patient,Report
from database.db import db

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
