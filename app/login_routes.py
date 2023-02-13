from flask_jwt_extended import create_access_token, get_jwt_identity
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.contact_routes import validate_request_body


login_bp = Blueprint("login_bp", __name__, url_prefix="/login")


@login_bp.route("", methods=["POST"])
def verify_user():
    request_body = request.get_json()
    user = validate_request_body(User, request_body)

    validated_user = User.query.filter_by(username=user.username).first()
    if not validated_user:
        response = {"msg": "Wrong username or password"}
        return jsonify(response)
    
    validated_user_json = validated_user.to_json()
    password = request.json.get("password")

    if validated_user_json["password"] == password:
        access_token = create_access_token(identity=validated_user_json["user_id"])
        response = {"access_token":access_token, "msg": "Successfully logged in."}
        return jsonify(response)