from ims.models.user import User
from ims.models.patient import Patient
from werkzeug.security import check_password_hash

class AuthService:

    @staticmethod
    def authenticate(username, password):
        # 1. Check User table
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        
        # 2. Check Patient table
        patient = Patient.query.filter_by(email=username).first()
        if patient and check_password_hash(patient.password, password):
            # You can wrap this in a pseudo-user object
            patient.role = "patient"
            return patient

        return None
