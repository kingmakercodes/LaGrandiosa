import os


class Config:
    SECRET_KEY= os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
    CORS_HEADERS= 'Content-Type'


class DevelopmentConfig(Config):
    DEBUG= True


class ProductionConfig(Config):
    DEBUG= False