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


class MailConfig:
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


class ReCAPTCHAConfig:
    RECAPTCHA_SECRET_KEY= os.getenv('RECAPTCHA_SECRET_KEY', 'your_google_recaptcha_secret_key')
    RECAPTCHA_VERIFICATION_URL= os.getenv('https://www.google.com/recaptcha/api/siteverify')