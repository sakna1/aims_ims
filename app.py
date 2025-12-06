from flask import Flask, render_template
from config import Config
from database.db import db
from flask_migrate import Migrate

# Import blueprints
from ims.auth.routes import auth_bp
from ims.admin.routes import admin_bp

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
    app.register_blueprint(admin_bp, url_prefix="/admin")  # <-- add this

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
