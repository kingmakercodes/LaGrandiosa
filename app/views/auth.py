import os
from flask import Blueprint, request, jsonify
import requests
from app import database, bcrypt
from app.models.models import User
from app.utils.email_utils import generate_verification_token, send_verification_email

auth_blueprint= Blueprint('auth', __name__)


# verify reCAPTCHA response
def verify_recaptcha(recaptcha_response):
    secret_key= os.getenv('RECAPTCHA_SECRET_KEY')
    data= {
        'secret': secret_key,
        'response': recaptcha_response
    }
    r= requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    return r.json().get('success')


# registration route
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data= request.get_json()
    username= data.get('username')
    email= data.get('email')
    password= data.get('password')
    recaptcha_response= data.get('recaptcha_response')

    user_exists= User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({'message':'User by this email already exists!'}),400

    if not verify_recaptcha(recaptcha_response):
        return jsonify({'message':'Invalid reCAPTCHA!'}), 400

    token= generate_verification_token(email)
    new_user= User(username=username, email=email)
    new_user.set_password(password)

    send_verification_email(email, token)
    if not send_verification_email(email, token):
        return jsonify({'message':'Email not verified! Please verify your email first!'}), 200

    database.session.add(new_user)
    database.session.commit()

