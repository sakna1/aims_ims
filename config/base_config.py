import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Use DATABASE_URL from env (Neon connection string)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:1234@localhost:5432/aims_db"  # fallback for local dev
    )
