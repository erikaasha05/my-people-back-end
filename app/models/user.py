from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    contacts = db.relationship("Contact", back_populates="user", lazy="select")

    def to_json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, user_data):
        return cls(
            username=user_data["username"],
            password=user_data["password"]
        )