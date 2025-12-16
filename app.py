from flask import Flask, render_template
from config import Config
from database.db import db
from flask_migrate import Migrate

# Import blueprints
from ims.auth.routes import auth_bp
from ims.admin.routes import admin_bp
from ims.patients.routes import patient_bp
from ims.billing.routes import billing_bp
from ims.images.routes import images_bp
from ims.staff.routes import staff_bp

# Import models
from ims.models.user import User
from ims.models.patient import Patient
from ims.models.image import Image
from ims.models.report import Report
from ims.models.billing import Billing
from ims.models.image_category import ImageCategory

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")  
    app.register_blueprint(patient_bp , url_prefix="/patient")
    app.register_blueprint(images_bp , url_prefix="/images")
    app.register_blueprint(billing_bp , url_prefix="/billing")
    app.register_blueprint(staff_bp , url_prefix="/staff")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

