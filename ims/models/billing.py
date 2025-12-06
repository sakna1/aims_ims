from datetime import datetime
from database.db import db

class Billing(db.Model):
    __tablename__ = "billing"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)

    task_name = db.Column(db.String(100), nullable=False)  # image upload, diagnosis, report
    cost_amount = db.Column(db.Float, nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", backref="billing_records")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "task_name": self.task_name,
            "cost_amount": self.cost_amount,
            "timestamp": self.timestamp
        }
