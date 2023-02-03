from flask_jwt_extended import unset_jwt_cookies
from app import db
from flask import Blueprint, jsonify

logout_bp = Blueprint("logout_bp", __name__, url_prefix="/logout")

@logout_bp.route("", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response