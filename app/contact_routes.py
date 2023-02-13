from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.contact import Contact
from app.models.reminder import Reminder

contacts_bp = Blueprint("contacts_bp", __name__, url_prefix="/contacts")

# Validate request body information
def validate_request_body(cls, request_body):
    try:
        new_model = cls.from_dict(request_body)
    except: 
        abort(make_response({"details": "Invalid data"}, 400))
    
    return new_model

# Validate id for models
def validate_id(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

@contacts_bp.route("", methods=["GET"])
# @jwt_required()
def read_all_contacts():
    contacts = Contact.query.all()
    contacts_response = [contact.to_json() for contact in contacts]

    return jsonify(contacts_response)

# refactored using jwt_required to add a contact to a user's profile
@contacts_bp.route("", methods=["POST"])
@jwt_required()
def create_contact_for_user():
    user_id = get_jwt_identity()
    request_body = request.get_json()

    new_contact = validate_request_body(Contact, request_body)
    new_contact.user_id = user_id

    db.session.add(new_contact)
    db.session.commit()

    new_contact_dict = new_contact.to_json()
    new_contact_dict["user_id"] = user_id

    return make_response(jsonify(new_contact.to_json()), 201)

# refactored using jwt_required to get a contact
@contacts_bp.route("/<contact_id>", methods=["GET"])
@jwt_required()
def read_one_contact(contact_id):
    contact = validate_id(Contact, contact_id)

    response = contact.to_json()

    return make_response(jsonify(response))

# refactored using jwt_required to update a contact
@contacts_bp.route("/<contact_id>", methods=["PUT"])
@jwt_required()
def update_one_contact(contact_id):
    contact = validate_id(Contact, contact_id)
    request_body = request.get_json()

    contact.first_name = request_body["first_name"]
    contact.last_name = request_body["last_name"]
    contact.number = request_body["number"]
    contact.email = request_body.get("email")
    contact.address = request_body.get("address")
    contact.birthday = request_body.get("birthday")
    contact.relationship = request_body.get("relationship")
    contact.notes = request_body.get("notes")
    contact.tags = request_body.get("tags")

    db.session.commit()

    return make_response(jsonify({"contact": contact.to_json()}))

# refactored using jwt_required to delete a contact for a user
@contacts_bp.route("/<contact_id>", methods=["DELETE"])
@jwt_required()
def delete_contact(contact_id):
    contact = validate_id(Contact, contact_id)

    db.session.delete(contact)
    db.session.commit()

    return make_response({"details":f"Contact {contact.contact_id}: \'{contact.first_name} {contact.last_name}\' successfully deleted"})

@contacts_bp.route("/<contact_id>/reminders", methods=["GET"])
def get_reminders_for_contact(contact_id):
    contact = validate_id(Contact, contact_id)

    reminders = [reminder.to_json() for reminder in contact.reminders]

    # maybe won't need below if to_json method is updated in models
    contact_dict = contact.to_json()
    contact_dict["reminders"] = reminders

    return make_response(jsonify(contact_dict))

@contacts_bp.route("/<contact_id>/reminders", methods=["POST"])
def create_reminders_for_a_contact(contact_id):
    contact = validate_id(Contact, contact_id)
    request_body = request.get_json()

    new_reminder = validate_request_body(Reminder, request_body)
    new_reminder.contact_id = contact_id

    db.session.add(new_reminder)
    db.session.commit()

    # maybe won't need below if to_json method is updated in models
    reminder_dict = new_reminder.to_json()
    # reminder_dict["contact_id"] = contact_id

    return make_response(jsonify(reminder_dict), 201)
