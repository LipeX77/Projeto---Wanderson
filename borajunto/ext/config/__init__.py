import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[3]


def init_app(app):
    env_name = os.getenv("FLASK_ENV", "development")

    if env_name == "testing":
        env_file = BASE_DIR / ".env.test"
    elif env_name == "production":
        env_file = BASE_DIR / ".env"
    else:
        env_file = BASE_DIR / ".env.dev"

    if env_file.exists():
        load_dotenv(env_file)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///borajunto.sqlite",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.getenv(
        "UPLOAD_FOLDER",
        str(BASE_DIR / "instance" / "uploads"),
    )
    app.config["MAX_CONTENT_LENGTH"] = int(
        os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024)
    )
    
    if os.getenv("TESTING") == "1":
        app.config["TESTING"] = True
    if os.getenv("WTF_CSRF_ENABLED") == "0":
        app.config["WTF_CSRF_ENABLED"] = False