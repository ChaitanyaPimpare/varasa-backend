from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

ADMIN_USER = "admin"
ADMIN_PASS = "varasa123"

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username == ADMIN_USER and password == ADMIN_PASS:
        token = create_access_token(identity=username)
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401
