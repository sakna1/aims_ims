from ims.models.user import User
from ims.models.patient import Patient
from werkzeug.security import check_password_hash
from flask import session

class AuthService:

    from ims.models.user import User
from ims.models.patient import Patient
from werkzeug.security import check_password_hash

class AuthService:

    @staticmethod
    def authenticate(username, password):
        print(f"[DEBUG] Attempting login for username: {username}")

        # 1. Check User table
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"[DEBUG] Found User: {user.username}, role: {user.role}")
            if check_password_hash(user.password_hash, password):
                print(f"[DEBUG] User password matched for {username}")
                return user
            else:
                print(f"[DEBUG] User password mismatch for {username}")
        else:
            print(f"[DEBUG] User not found in User table for username: {username}")

        # 2. Check Patient table
        patient = Patient.query.filter_by(username=username).first()
        if patient:
            print(f"[DEBUG] Found Patient: {patient.username}")
            if check_password_hash(patient.password_hash, password):
                patient.role = "patient"  # Assign role for session
                print(f"[DEBUG] AUTHENTICATED PATIENT ROLE: {patient.role}")
                return patient
            else:
                print(f"[DEBUG] Patient password mismatch for {username}")
        else:
            print(f"[DEBUG] Patient not found in Patient table for username: {username}")

        print(f"[DEBUG] Login failed for username: {username}")
        return None

    
    def logout():
        """Clear session and log out user."""
        session.clear()
        return True
