from functools import wraps
from flask import request, jsonify
from backend.app.models.models import User
from flask import current_app
import jwt
import os
import requests


# fetch token from headers
def fetch_token():
    token= request.headers.get('Authorization')

    if not token:
        return None, jsonify({'message':'Token is missing!'}), 403
    return token, None, None


# function to verify token
def verify_token(token):
    try:
        payload= jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        current_user= User.query.get(payload['user_id'])

        if not current_user:
            raise jwt.InvalidTokenError('User does not exist!')
        return current_user, None, None
    except jwt.ExpiredSignatureError:
        return None, jsonify({'message':'Token has expired!'}), 403
    except jwt.InvalidTokenError:
        return None, jsonify({'message':'Invalid token!'}), 403


# token requirement function
def token_required(f):
    @wraps(f)

    def decorated(*args, **kwargs):
        # fetch the token
        token, error_response, status_code= fetch_token()

        if error_response:
            return error_response, status_code

        # verify the token
        current_user, error_response, status_code= verify_token(token)
        if error_response:
            return error_response, status_code

        # pass current user to decorated function
        return f(current_user, *args, **kwargs)

    return decorated()


# reCAPTCHA verification logic
def verify_recaptcha(recaptcha_response):
    # verification using Google's API
    secret_key= current_app.config['RECAPTCHA_SECRET_KEY']
    verification_url= current_app.config['RECAPTCHA_VERIFICATION_URL']

    payload= {'secret': secret_key, 'response': recaptcha_response}
    response= requests.post(verification_url, data=payload)
    return response.json()