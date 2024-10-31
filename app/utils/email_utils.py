import os
import jwt
from flask import url_for
from flask_mail import Message
from datetime import datetime, timedelta
from app import mail


# generate a verification token
def generate_verification_token(email, password):
    payload= {
        'email':email,
        'password': password,
        'exp': datetime.now()+ timedelta(hours=24)
    }
    return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

# send verification email
def send_verification_email(email, token):
    verification_url= url_for('auth.verify_email', token=token, _external=True)
    msg= Message('Email Verification', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
    msg.body= f'Please follow this link to verify your email: {verification_url}'
    mail.send(msg)


# decode verification token to get email and password payloads
def decode_verification_token(token):
    try:
        return jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None # to handle expiration outside the function
    except jwt.InvalidTokenError:
        return None # to handle invalid token outside the function