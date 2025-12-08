from ims.models import Image
from database.db import db

class ImageService:

    @staticmethod
    def get_images_by_patient_id(patient_id):
        """
        Return all medical images uploaded under a specific patient.
        """
        return Image.query.filter_by(patient_id=patient_id).order_by(Image.timestamp.desc()).all()
