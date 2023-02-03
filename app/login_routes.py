from flask_jwt_extended import create_access_token
from app import db
from flask import Blueprint, request, jsonify

login_bp = Blueprint("login_bp", __name__, url_prefix="/login")


@login_bp.route("", methods=["POST"])
def create_user():
    username = request.json.get("username")
    password = request.json.get("password")
    if username != "test" or password != "test":
        return {"msg": "Wrong username or password"}, 401

    access_token = create_access_token(identity=username)
    response = {"access_token":access_token}
    return jsonify(response)