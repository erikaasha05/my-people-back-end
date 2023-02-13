from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, create_access_token
from datetime import datetime, timedelta, timezone

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "remember-to-change-this"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    # else:
    #     app.config["TESTING"] = True
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #         "SQLALCHEMY_TEST_DATABASE_URI")

    # if "RDS_DB_NAME" in os.environ:
    #     app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
    #     username=os.environ['RDS_USERNAME'],
    #     password=os.environ['RDS_PASSWORD'],
    #     host=os.environ['RDS_HOSTNAME'],
    #     port=os.environ['RDS_PORT'],
    #     database=os.environ['RDS_DB_NAME'],
    # )
    # else:
    #     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app.models.contact import Contact
    from app.models.reminder import Reminder
    from app.models.user import User

    # Register Blueprints
    from app.contact_routes import contacts_bp
    from app.reminder_routes import reminders_bp
    from app.user_routes import users_bp
    from app.login_routes import login_bp
    from app.logout_routes import logout_bp
    app.register_blueprint(contacts_bp)
    app.register_blueprint(reminders_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                data = response.get_json()
                if type(data) is dict:
                    data["access_token"] = access_token
                    response.data = json.dumps(data)
            
            return response
        except (RuntimeError, KeyError):
            return response

    CORS(app)
    return app