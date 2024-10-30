from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import DevelopmentConfig
from flask_migrate import Migrate

migrate= Migrate()
database= SQLAlchemy()
jwt= JWTManager()

def create_app():
    app= Flask(__name__)

    # configure flask application
    app.config.from_object(DevelopmentConfig)

    # initialise global app instances
    database.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, database)
    CORS(app)

    with app.app_context():
        # import routes and models here
        from app.models.models import User, Category, Product, Cart, CartItem, Order, OrderItem
        database.create_all()

    return app