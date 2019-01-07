from flask import request, jsonify, make_response
from marshmallow import Schema, fields
from datetime import datetime, timedelta
from functools import wraps
import jwt
import os

SECRET_KEY = os.getenv('SECRET_KEY')


def generate_token(self, user_id, is_admin):

    """ Generates the access token"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=120),
            'iat': datetime.utcnow(),
            'user': {
                'user_id': user_id,
                'is_admin': is_admin
            }
        }
        # create the byte string token using the payload and the SECRET key
        jwt_string = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
        return jwt_string

    except Exception as e:
        # return an error in string format if an exception occurs
        return str(e)


def decode_token(token):

    """Decodes the access token from the Authorization header."""

    try:
        # try to decode the token using our SECRET variable
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user']
    except jwt.ExpiredSignatureError:
        # the token is expired, return an error string
        return "Expired token. Please login to get a new token"
    except jwt.InvalidTokenError:
        # the token is invalid, return an error string
        return "Invalid token"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access = request.headers.get('Authorization')
        if not access:
            return make_response(jsonify({
                "message": "Authorization required!",
            }), 401)

        token = access.split(" ")[1]
        # ensure token is present
        if not token:
            return make_response(jsonify({
                "message": "token is missing!",
            }), 401)
        
        user = decode_token(token)
        if isinstance(user, str):
            return make_response(jsonify({
                "message": "unsuccessful",
                "error": user
            }), 401)

        return f(user=user, *args, **kwargs)
       
    return decorated


# for serialization
class IncidentSchema(Schema):
    id = fields.Int()
    createdBy = fields.Int()
    createdOn = fields.DateTime()
    type_of_incident = fields.Str()
    location = fields.Str()
    status = fields.Str()
    images = fields.Str()
    videos = fields.Str()
    comment = fields.Str()