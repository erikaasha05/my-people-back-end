from app import db

class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    number = db.Column(db.String(20))
    email = db.Column(db.String(50), nullable = True)
    address = db.Column(db.String(250), nullable = True)
    birthday = db.Column(db.String(50), nullable = True)
    relationship = db.Column(db.ARRAY(db.String), nullable = True)
    notes = db.Column(db.String(500), nullable = True)
    tags = db.Column(db.ARRAY(db.String), nullable = True)
    reminders = db.relationship("Reminder", back_populates="contact", lazy="select")
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = True)
    user = db.relationship("User", back_populates="contacts")

    def to_json(self):
        return {
            "contact_id": self.contact_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "number": self.number,
            "email": self.email,
            "address": self.address,
            "birthday": self.birthday,
            "relationship": self.relationship,
            "notes": self.notes,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, contact_data):
        return cls(
            first_name=contact_data["first_name"],
            last_name=contact_data["last_name"],
            number=contact_data["number"],
            email=contact_data.get("email"),
            address=contact_data.get("address"),
            birthday=contact_data.get("birthday"),
            relationship=contact_data.get("relationship"),
            notes=contact_data.get("notes"),
            tags=contact_data.get("tags")
        )
