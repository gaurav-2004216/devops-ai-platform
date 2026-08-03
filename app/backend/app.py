from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response, request
import time
from prometheus_flask_exporter import PrometheusMetrics

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
metrics = PrometheusMetrics(app)
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency",
    ["endpoint"]
)

app.config.from_object(Config)
app.config["UPLOAD_FOLDER"] = "uploads"

jwt = JWTManager(app)

db.init_app(app)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(main_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(ai_bp)
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(
        request.method,
        request.path,
        response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        request.path
    ).observe(time.time() - request.start_time)

    return response
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
@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
