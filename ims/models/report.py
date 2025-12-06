from datetime import datetime
from database.db import db

class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    report_text = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.String(255))
    status = db.Column(db.String(50), default="Draft")  # Draft or Confirmed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", backref="reports")
    user = db.relationship("User", backref="reports_created")
    image = db.relationship("Image", backref="report")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "image_id": self.image_id,
            "created_by": self.created_by,
            "report_text": self.report_text,
            "diagnosis": self.diagnosis,
            "status": self.status,
            "created_at": self.created_at
        }
