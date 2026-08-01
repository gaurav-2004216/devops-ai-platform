from flask import Blueprint, request, jsonify
from models import User
from database import db
import bcrypt

register_bp = Blueprint("register",__name__)


@register_bp.route("/register",methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}),400

    existing = User.query.filter_by(email=email).first()

    if existing:
        return jsonify({"error": "Email already exists"}),409

    hashed_password =  bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
       ).decode("utf-8")

    user = User(
            username=username,
            email=email,
            password=hashed_password
            )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
        }),201
