from datetime import datetime
from database.db import db

class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('image_categories.id'))

    file_path = db.Column(db.String(255), nullable=False)
    image_type = db.Column(db.String(50))   # MRI, CT, X-ray
    disease_type = db.Column(db.String(100))  # lung cancer, brain tumor etc.

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", backref="images")
    user = db.relationship("User", backref="uploaded_images")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "uploaded_by": self.uploaded_by,
            "file_path": self.file_path,
            "image_type": self.image_type,
            "disease_type": self.disease_type,
            "timestamp": self.timestamp
        }
