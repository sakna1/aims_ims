from datetime import datetime
from database.db import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(255))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    conditions = db.Column(db.Text)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_by_user = db.relationship("User", backref="created_patients")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "dob": self.dob,
            "gender": self.gender,
            "conditions": self.conditions,
            "registration_date": self.registration_date,
            "created_by": self.created_by
        }
