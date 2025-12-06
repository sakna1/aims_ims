class BaseConfig:
    SECRET_KEY = "your-secret-key"

    # PostgreSQL connection
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:1234@localhost:5432/aims_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
