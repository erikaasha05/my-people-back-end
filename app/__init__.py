from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # if test_config is None:
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #         "SQLALCHEMY_DATABASE_URI")
    # else:
    #     app.config["TESTING"] = True
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #         "SQLALCHEMY_TEST_DATABASE_URI")

    if "RDS_DB_NAME" in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
        username=os.environ['RDS_USERNAME'],
        password=os.environ['RDS_PASSWORD'],
        host=os.environ['RDS_HOSTNAME'],
        port=os.environ['RDS_PORT'],
        database=os.environ['RDS_DB_NAME'],
    )
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app.models.contact import Contact
    from app.models.reminder import Reminder
    from app.models.user import User

    # Register Blueprints
    from app.contact_routes import contacts_bp
    from app.reminder_routes import reminders_bp
    app.register_blueprint(contacts_bp)
    app.register_blueprint(reminders_bp)

    CORS(app)
    return app