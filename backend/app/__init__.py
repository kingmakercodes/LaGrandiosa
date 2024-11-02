from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from backend.app.config import DevelopmentConfig, MailConfig, ReCAPTCHAConfig
from flask_migrate import Migrate
from flask_mail import Mail

mail= Mail()
migrate= Migrate()
database= SQLAlchemy()
jwt= JWTManager()

def create_app():
    app= Flask(__name__)

    # configure flask application
    app.config.from_object(DevelopmentConfig)

    # configure flask mail application
    app.config.from_object(MailConfig)

    # configure recaptcha settings for application
    app.config.from_object(ReCAPTCHAConfig)

    # initialise global app instances
    mail.init_app(app)
    database.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, database)
    CORS(app)

    # register blueprints
    from backend.app.views.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        # import routes and models here
        database.create_all()

    return app