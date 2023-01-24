
from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.contact import Contact

contacts_bp = Blueprint("contacts_bp", __name__, url_prefix="/contacts")

# Validate request body information
def validate_request_body(cls, request_body):
    try:
        new_model = cls.create_contact(request_body)
    except: 
        abort(make_response({"details": "Invalid data"}, 400))
    
    return new_model

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

    return make_response(jsonify(new_contact.to_json), 201)

