from database.db import db

class ImageCategory(db.Model):
    __tablename__ = "image_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    images = db.relationship("Image", backref="category", lazy=True)
