from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.reminder import Reminder
from app.contact_routes import validate_id, validate_request_body

reminders_bp = Blueprint("reminders_bp", __name__, url_prefix="/reminders")

@reminders_bp.route("", methods=["GET"])
def read_all_reminders():
    reminders = Reminder.query.all()
    reminders_response = [reminder.to_json() for reminder in reminders]

    return jsonify(reminders_response)

@reminders_bp.route("", methods=["POST"])
def create_reminder():
    request_body = request.get_json()

    new_reminder = validate_request_body(Reminder, request_body)

    db.session.add(new_reminder)
    db.session.commit()

    return make_response(jsonify(new_reminder.to_json()), 201)

@reminders_bp.route("/<reminder_id>", methods=["GET"])
def read_one_reminder(reminder_id):
    reminder = validate_id(Reminder, reminder_id)

    response = reminder.to_json()

    return make_response(jsonify(response))

@reminders_bp.route("/<reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    reminder = validate_id(Reminder, reminder_id)

    db.session.delete(reminder)
    db.session.commit()

    return make_response({"details":f"Reminder {reminder.reminder_id}: \'{reminder.message}\' successfully deleted"})

