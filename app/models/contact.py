from app import db

class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    number = db.Column(db.Integer)
    email = db.Column(db.String(50), nullable = True)
    address = db.Column(db.String(250), nullable = True)
    birthday = db.Column(db.DateTime, nullable = True)
    relationship = db.Column(db.ARRAY(db.String), nullable = True)
    notes = db.Column(db.String(500), nullable = True)
    tags = db.Column(db.ARRAY(db.String), nullable = True)
