# ims/staff/service.py
import os
from werkzeug.utils import secure_filename
from ims.models import Patient,Report,Image,User
from database.db import db
from sqlalchemy.exc import SQLAlchemyError

class StaffService:

       
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
    
    #admin

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