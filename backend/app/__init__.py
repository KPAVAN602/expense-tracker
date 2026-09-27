import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import db, jwt

load_dotenv()

def create_app():
    app = Flask(__name__)

    # MYSQL configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")   # <-- fixed: URI not URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT configuration — must be set before jwt.init_app(app)
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register Authentication Routes
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Create Tables
    with app.app_context():
        db.create_all()

    return app