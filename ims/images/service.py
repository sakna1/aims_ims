import os
from werkzeug.utils import secure_filename
from ims.models import Image, Patient ,ImageCategory
from database.db import db
from flask import url_for

class ImageService:

    @staticmethod
    def get_images_by_patient_id(patient_id):
        """
        Return all medical images uploaded under a specific patient.
        """
        return Image.query.filter_by(patient_id=patient_id).order_by(Image.timestamp.desc()).all()
    
    @staticmethod
    def upload_images(patient_id, uploaded_by, images, image_type, description):
        saved_files = []

        upload_folder = r"D:\sakna\Sakna Perera\Lec\Software Architecture and Programming\CW2\AIMS\abc_ims\uploads"

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        for img in images:
            filename = secure_filename(img.filename)

            file_path = os.path.join(upload_folder, filename)
            img.save(file_path)

            db_path = url_for("images_bp.view_file", filename=filename)

            new_image = Image(
                patient_id=patient_id,
                uploaded_by=uploaded_by,
                file_path=db_path,
                image_type=image_type,
                description=description
            )

            db.session.add(new_image)
            saved_files.append(filename)

        db.session.commit()
        return saved_files

    @staticmethod
    def get_uploaded_images(staff_id):    
       return Image.query.filter_by(uploaded_by=staff_id).order_by(Image.timestamp.desc()).all()
    
    @staticmethod
    def get_all_patients():
        return Patient.query.all()
    
    @staticmethod
    def get_all_images():
      return Image.query.order_by(Image.id.desc()).all()
    
    @staticmethod
    def delete_image(image_id):
        image = Image.query.get(image_id)
        if not image:
            return False

        # Physical upload folder
        upload_folder = r"D:\sakna\Sakna Perera\Lec\Software Architecture and Programming\CW2\AIMS\abc_ims\uploads"

        # Full path on disk
        filename = os.path.basename(image.file_path)
        file_path = os.path.join(upload_folder, filename)

        # Delete file from disk
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete from DB
        db.session.delete(image)
        db.session.commit()
        return True
    
    @staticmethod
    def get_all_categories():
        return ImageCategory.query.all()
    
    @staticmethod
    def get_images_without_report():
        from ims.models import Report  
        return Image.query.filter(
            ~Image.id.in_(db.session.query(Report.image_id))
        ).all()


 

    


