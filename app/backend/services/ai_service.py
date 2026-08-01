from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

ai_bp = Blueprint("ai", __name__)


def generate_recommendations(report):

    recommendations = []

    tools = report.get("tools", {})

    if not tools.get("docker"):
        recommendations.append({
            "title": "Docker",
            "priority": "High",
            "message": "Create a Dockerfile to containerize your application."
        })

    if not tools.get("docker_compose"):
        recommendations.append({
            "title": "Docker Compose",
            "priority": "Medium",
            "message": "Use docker-compose.yml for local multi-container development."
        })

    if not tools.get("terraform"):
        recommendations.append({
            "title": "Terraform",
            "priority": "High",
            "message": "Provision infrastructure using Terraform."
        })

    if not tools.get("kubernetes"):
        recommendations.append({
            "title": "Kubernetes",
            "priority": "High",
            "message": "Deploy your application using Kubernetes manifests."
        })

    if not tools.get("jenkins"):
        recommendations.append({
            "title": "CI/CD",
            "priority": "High",
            "message": "Add a Jenkins pipeline for automated builds and deployments."
        })

    if not tools.get("github_actions"):
        recommendations.append({
            "title": "GitHub Actions",
            "priority": "Low",
            "message": "Automate testing using GitHub Actions."
        })

    if report["score"] >= 80:
        overall = "Excellent DevOps maturity."

    elif report["score"] >= 60:
        overall = "Good project. Some improvements are recommended."

    else:
        overall = "Project needs DevOps improvements."

    return {
        "overall": overall,
        "recommendations": recommendations
    }


@ai_bp.route("/ai/review", methods=["POST"])
@jwt_required()
def review():

    report = request.get_json()

    return jsonify(generate_recommendations(report))
