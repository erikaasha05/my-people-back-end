
from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.contact import Contact

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
def read_all_contacts():
    contacts = Contact.query.all()
    contacts_response = [contact.to_json() for contact in contacts]

    return jsonify(contacts_response)

@contacts_bp.route("", methods=["POST"])
def create_contact():
    request_body = request.get_json()

    new_contact = validate_request_body(Contact, request_body)

    db.session.add(new_contact)
    db.session.commit()

    return make_response(jsonify(new_contact.to_json()), 201)

@contacts_bp.route("/<contact_id>", methods=["GET"])
def read_one_contact(contact_id):
    contact = validate_id(Contact, contact_id)

    response = contact.to_json()

    return make_response(jsonify(response))

@contacts_bp.route("/<contact_id>", methods=["PATCH"])
def update_one_contact(contact_id):
    pass

@contacts_bp.route("/<contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    contact = validate_id(Contact, contact_id)

    db.session.delete(contact)
    db.session.commit()

    return make_response({"details":f"Contact {contact.contact_id}: {contact.first_name} {contact.last_name} successfully deleted"})