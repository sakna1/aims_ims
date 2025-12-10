# ims/staff/service.py
import os
from werkzeug.utils import secure_filename
from ims.models import Patient,Report,Image
from database.db import db

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

    
