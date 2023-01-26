from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models
    from app.models.contact import Contact
    from app.models.reminder import Reminder


    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from .contact_routes import contacts_bp
    from .reminder_routes import reminders_bp
    app.register_blueprint(contacts_bp)
    app.register_blueprint(reminders_bp)

    CORS(app)
    return app