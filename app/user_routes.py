from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app.models.contact import Contact
from app.contact_routes import validate_id, validate_request_body

users_bp = Blueprint("users_bp", __name__, url_prefix="/users")

@users_bp.route("", methods=["GET"])
def read_all_users():
    users = User.query.all()
    users_response = [user.to_json() for user in users]

    return jsonify(users_response)

@users_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()

    new_user = validate_request_body(User, request_body)

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify(new_user.to_json()), 201)

@users_bp.route("/<user_id>", methods=["GET"])
def read_one_user(user_id):
    user = validate_id(User, user_id)

    response = user.to_json()

    return make_response(jsonify(response))

@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = validate_id(User, user_id)

    db.session.delete(user)
    db.session.commit()

    return make_response({"details":f"User {user.user_id}: \'{user.username}\' successfully deleted"})

@users_bp.route("/<username>/contacts", methods=["GET"])
def get_contacts_for_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(make_response({"message":f"User {username} not found"}, 404))
    
    contacts = [contact.to_json() for contact in user.contacts]

    user_dict = user.to_json()
    user_dict["contacts"] = contacts

    return make_response(jsonify(user_dict))

