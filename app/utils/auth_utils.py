from functools import wraps
from flask import request, jsonify
from app.models.models import User
import jwt
import os

# token requirement function
def token_required(f):
    @wraps(f)

    def decorated(*args, **kwargs):
        token= request.headers.get('Authorization')

        if not token:
            return jsonify({'message':'Token is missing!'}), 403

        try:
            payload= jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            current_user= User.query.get(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message':'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message':'Invalid token!'}), 403

        return f(current_user, *args, **kwargs)
    return decorated