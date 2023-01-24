from app import db

class Reminder(db.Model):
    reminder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(500))
    date = db.Column(db.String(20))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.contact_id'), nullable = True)
    contact = db.relationship("Contact", back_populates="reminders")