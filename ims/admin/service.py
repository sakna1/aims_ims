# ims/admin/service.py
from database.db import db
from ims.models import User, Patient,ImageCategory

class AdminService:
    
    @staticmethod
    def total_patients_count():
        return db.session.query(db.func.count(Patient.id)).scalar() or 0
    
    @staticmethod
    def create_category(name):
        # Check if category already exists
        existing = ImageCategory.query.filter_by(name=name).first()
        if existing:
            return None  # Or raise custom exception

        new_category = ImageCategory(name=name)
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def list_categories():
     return ImageCategory.query.order_by(ImageCategory.id.desc()).all()
    
    @staticmethod
    def get_category(id):
        return ImageCategory.query.get(id)
    
    @staticmethod
    def update_category(category_id, **kwargs):
        category = ImageCategory.query.get(category_id)
        if not category:
            return None

        for field, value in kwargs.items():
            if hasattr(category, field) and value is not None:
                setattr(category, field, value)

        try:
            db.session.commit()
            return category
        except:
            db.session.rollback()
            return None

    @staticmethod
    def delete_category(category_id):
        category = ImageCategory.query.get(category_id)
        if not category:
            return False

        try:
            db.session.delete(category)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
        
    @staticmethod
    def count_patients():
        return Patient.query.count()

    @staticmethod
    def count_staff():
        return User.query.count()   
    
    @staticmethod
    def count_categories():
        return ImageCategory.query.count()   


