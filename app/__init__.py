from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import DevelopmentConfig, MailConfig
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bcrypt import Bcrypt


bcrypt= Bcrypt()
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

    # initialise global app instances
    bcrypt.init_app(app)
    mail.init_app(app)
    database.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, database)
    CORS(app)

    # register blueprints
    from app.views.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        # import routes and models here
        from app.models.models import User, Category, Product, Cart, CartItem, Order, OrderItem
        database.create_all()

    return app