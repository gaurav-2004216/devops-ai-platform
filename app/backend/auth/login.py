from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
import bcrypt

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    print("Email:", email)

    user = User.query.filter_by(email=email).first()

    print("User:", user)

    if not user:
        print("User not found")
        return jsonify({"error":"Invalid email or password"}),401

    print("DB Password:", repr(user.password))
    print("Entered Password:", repr(password))

    match = bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8")
    )

    print("Password Match:", match)

    if not match:
        return jsonify({"error":"Invalid email or password"}),401

    access_token = create_access_token(identity=user.email)

    return jsonify({
        "message":"Login successful",
        "access_token":access_token
    }),200
