import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()  # reads the .env file


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-key")

    _user = os.getenv("DB_USER", "root")
    _password = quote_plus(os.getenv("DB_PASSWORD", ""))
    _host = os.getenv("DB_HOST", "localhost")
    _port = os.getenv("DB_PORT", "3306")
    _name = os.getenv("DB_NAME", "foodexpress_db")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{_user}:{_password}@{_host}:{_port}/{_name}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secure session cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB upload limit (used for food images later)
