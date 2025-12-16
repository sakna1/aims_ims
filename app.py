import os

from flask import Flask, render_template
from database.db import db

# Import blueprints
from ims.auth.routes import auth_bp
from ims.admin.routes import admin_bp
from ims.patients.routes import patient_bp
from ims.billing.routes import billing_bp
from ims.images.routes import images_bp
from ims.staff.routes import staff_bp


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # Database config – Neon connection string must be in env var DATABASE_URL
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init SQLAlchemy
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(patient_bp, url_prefix="/patient")
    app.register_blueprint(images_bp, url_prefix="/images")
    app.register_blueprint(billing_bp, url_prefix="/billing")
    app.register_blueprint(staff_bp, url_prefix="/staff")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()

if __name__ == "__main__":
    # For local dev; in Cloud Run gunicorn will run `app:app`
    app.run(host="0.0.0.0", port=8080)
