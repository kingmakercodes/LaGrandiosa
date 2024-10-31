import os
from tkinter.ttk import Label

from flask import Blueprint, request, jsonify
import requests
from app import database, bcrypt
from app.models.models import User
from app.utils.email_utils import generate_verification_token, send_verification_email, decode_verification_token

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


# verify email
@auth_blueprint.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try:
        # decode the token to get the email
        payload= decode_verification_token(token)
        email= payload.get['email']

        # check if email is already verified and registered
        if User.query.filter_by(email=email).first():
            return jsonify({'message':'Email is already in use!'}), 400

        # create user and add to database
        return jsonify({'message':'Email verified successfully!'}), 200

    except None:
        return jsonify({'message':'Invalid or expired token!'}), 400

# registration route
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data= request.get_json()
    username= data.get('username')
    email= data.get('email')
    password= data.get('password')
    recaptcha_response= data.get('recaptcha_response')

    user_exists= User.query.filter_by(email=email).first()

    if not verify_recaptcha(recaptcha_response):
        return jsonify({'message':'Invalid reCAPTCHA!'}), 400

    # verify if user already exists
    if user_exists:
        return jsonify({'message':'User already exists!'}), 400

    token= generate_verification_token(email)
    send_verification_email(email, token)

    new_user= User(username=username, email=email)
    new_user.set_password(password)

    database.session.add(new_user)
    database.session.commit()

    return jsonify({'message':'User account verified, registration complete!'}), 200