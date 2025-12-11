# ims/staff/service.py
import os
from werkzeug.utils import secure_filename
from ims.models import Patient,Report,Image
from database.db import db
from sqlalchemy import or_

class StaffService:

    @staticmethod
    def get_all_patients():
        return Patient.query.all()
    
    @staticmethod
    def save_report(patient_id, image_id, created_by, report_text, diagnosis):
        report = Report.query.filter_by(image_id=image_id).first()

        if report:
            report.report_text = report_text
            report.diagnosis = diagnosis
            report.status = "Draft"
        else:
            report = Report(
                patient_id=patient_id,
                image_id=image_id,
                created_by=created_by,
                report_text=report_text,
                diagnosis=diagnosis,
                status="Draft"
            )
            db.session.add(report)

        db.session.commit()
        return report


    # Get all reports created by radiologist
    @staticmethod
    def get_reports_by_radiologist(user_id):
        return (
            Report.query
            .filter_by(created_by=user_id)
            .order_by(Report.created_at.desc())
            .all()
        )

    @staticmethod
    def get_image(image_id):
     return Image.query.get(image_id)
    
    @staticmethod
    def get_report_by_image(image_id):
        return Report.query.filter_by(image_id=image_id).first()     

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
        if query.isdigit():
            return Patient.query.filter_by(id=int(query)).first()
        return Patient.query.filter(Patient.name.ilike(f"%{query}%")).first()
    
    @staticmethod
    def get_images_by_patient(patient_id):
        return Image.query.filter_by(patient_id=patient_id).order_by(Image.timestamp.desc()).all()

    @staticmethod
    def get_reports_by_patient(patient_id):
        return Report.query.filter_by(patient_id=patient_id).all()

    @staticmethod
    def create_report(patient_id, image_id, user_id, report_text):
        report = Report(
            patient_id=patient_id,
            image_id=image_id,
            created_by=user_id,
            report_text=report_text,
            status="Draft"
        )
        db.session.add(report)
        db.session.commit()
        return report

    @staticmethod
    def update_report(report_id, disease_type, diagnosis, status):
        report = Report.query.get(report_id)
        if report:
            report.disease_type = disease_type
            report.diagnosis = diagnosis
            report.status = status
            db.session.commit()
        return report
