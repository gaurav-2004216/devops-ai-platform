from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

load_dotenv()

from config import Config
from database import db
from models import User
from auth.register import register_bp
from auth.login import login_bp
from routes import main_bp
from upload import upload_bp
from services.ai_service import ai_bp

app = Flask(__name__)

app.config.from_object(Config)
app.config["UPLOAD_FOLDER"] = "uploads"

jwt = JWTManager(app)

db.init_app(app)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(main_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(ai_bp)

@app.route("/")
def home():
    return {
        "message": "Welcome to AI DevSecOps Platform",
        "status": "Running"
    }

@app.route("/health")
def health():
    return {
        "status": "healthy"
    }

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
