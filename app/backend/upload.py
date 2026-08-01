from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
import zipfile
import shutil

from services.analyzer import analyze_project

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {
    "zip",
    "py",
    "txt",
    "json",
    "yaml",
    "yml",
    "dockerfile"
}


def allowed_file(filename):
    if "." not in filename:
        return filename.lower() == "dockerfile"

    return filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():

    # Check file exists
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Check filename
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Validate extension
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)

    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    # Save uploaded file
    file.save(upload_path)

    # If ZIP, extract it
    if filename.endswith(".zip"):

        extract_folder = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            filename.replace(".zip", "")
        )

        # Remove previous extraction if exists
        if os.path.exists(extract_folder):
            shutil.rmtree(extract_folder)

        os.makedirs(extract_folder)

        with zipfile.ZipFile(upload_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)

        # Analyze extracted project
        report = analyze_project(extract_folder)

    else:
        # Analyze single file
        else:
    report = {
        "checks": ["Single file uploaded"],
        "recommendations": [],
        "score": 10,
        "language": "Unknown"
    }

    return jsonify({
        "message": "Upload successful",
        "analysis": report
    }), 200
