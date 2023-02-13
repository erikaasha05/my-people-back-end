from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import User
from app.models.contact import Contact
from app.models.reminder import Reminder
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
    user = validate_request_body(User, request_body)

    new_user = User.query.filter_by(username=user.username).first()

    # return make_response(f"{user.to_json()} and {request_body} and {new_user}")

    if not new_user:
        db.session.add(user)
        db.session.commit()

        return make_response("Successfully registered. Please sign in.", 201)
    else:
        return make_response("User already exists. Please sign in.", 202)

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

@users_bp.route("/contacts", methods=["GET"])
@jwt_required()
def get_contacts_for_user():
    user_id = get_jwt_identity()
    # return jsonify(logged_in_as=current_user), 200
    current_user = User.query.get(user_id)

    contacts = [contact for contact in current_user.contacts]
    reminders = []

    for contact in contacts:
        for reminder in contact.reminders:
            reminders.append(reminder.to_json())

    contact_dict = [contact.to_json() for contact in contacts]
    user_dict = current_user.to_json()
    user_dict["contacts"] = contact_dict
    user_dict["reminders"] = reminders

    return make_response(jsonify(user_dict))

# @users_bp.route("/reminders", methods=["GET"])
# def get_all_reminders_for_user():
#     user_id = get_jwt_identity()
#     current_user = User.query.get(user_id)

