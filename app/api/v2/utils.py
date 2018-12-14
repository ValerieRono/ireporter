from functools import wraps
from flask import request, jsonify, make_response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access = request.headers.get('Authorization')
        if not access:
            return jsonify({'message': 'Authorization required!'}), 401

        token = access.split(" ")[1]
        # ensure token is present
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        user = Users.decode_token(token)
        if isinstance(user, str):
            return make_response(jsonify({
                "message": "invalid token",
                "error": user
            }), 400)

        return f(user=user, *args, **kwargs)
       
    return decorated