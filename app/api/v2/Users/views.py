from flask import abort, current_app
from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse, marshal, inputs
from marshmallow import Schema, fields
from functools import wraps

# local import
from app.api.v2.Users.models import record_fields, Users, ManipulateDbase

record_parser = reqparse.RequestParser()

record_parser.add_argument(
    'firstname',
    required=True,
    help='please provide input',
    type=str,
    location='json'
    )
record_parser.add_argument(
    'lastname',
    required=True,
    help='please provide input',
    type=str,
    location='json'
    )
record_parser.add_argument(
    'othernames',
    required=True,
    help='please provide input',
    type=str,
    location='json'
    )
record_parser.add_argument(
    'email',
    required=True,
    help='please provide input',
    type=str,
    location='json'
    )
record_parser.add_argument(
    'phoneNumber',
    required=True,
    help='please provide input',
    type=str,
    location='json'
    )
record_parser.add_argument(
    'username',
    required=True,
    help='please comment',
    type=str,
    location='json'
    )
record_parser.add_argument(
    'password',
    required=True,
    help='password required',
    type=str,
    location='json'
    )

edit_parser = reqparse.RequestParser()

edit_parser.add_argument(
    'firstname',
    type=str,
    location='json')
edit_parser.add_argument(
    'lastname',
    type=str,
    location='json')
edit_parser.add_argument(
    'othernames',
    type=str,
    location='json'
    )
edit_parser.add_argument(
    'email',
    type=str,
    location='json'
    )
edit_parser.add_argument(
    'phoneNumber',
    type=str,
    location='json'
    )
edit_parser.add_argument(
    'username',
    type=str,
    location='json'
    )
edit_parser.add_argument(
    'password',
    type=str,
    location='json'
    )

# for serialization
class IncidentSchema(Schema):
    id = fields.Int()
    firstname = fields.Str()
    lastname = fields.Str()
    othernames = fields.Str()
    email = fields.Str()
    phoneNumber = fields.Str()
    username = fields.Str()
    password = fields.Str()
    registered = fields.DateTime()
    isAdmin = fields.Boolean()


incident_Schema = IncidentSchema()
incidents_Schema = IncidentSchema(many=True)

manipulate = ManipulateDbase()


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


class MyUsers(Resource):
    def __init__(self):
        super(MyUsers, self).__init__()
        self.parser = record_parser

    def get(self):
        response = manipulate.fetch()
        return {
            "status": 200,
            "data": [{"incidents": response, "message": "successfull"}]
        }, 200

    def post(self):
        args = self.parser.parse_args()
        # query to see if user exists
        # user = manipulate.find_by_email(args['email'])
        # if not user:
        keys = args.keys()
        for key in keys:
            if not args[key]:
                return {
                    "status": 404,
                    "data": [{"message": "please provide input"}]
                }, 404
            user = Users(
                firstname=args['firstname'],
                lastname=args['lastname'],
                othernames=args['othernames'],
                email=args['email'],
                phoneNumber=args['phoneNumber'],
                username=args['username'],
                password=args['password']
            )
        new_user = incident_Schema.dump(user).data

        # # hash password and store the hashed password with the user
        # user.hash_password()

        save_user = manipulate.save(new_user)
        result = marshal(save_user, record_fields)
        return {
            'status': 201,
            'data': [{"user": result, "message": "registered user"}]
        }, 201

        # return {
        #     'message': 'user with email exists, proceed to log in'
        # }, 401


class login(Resource):
    # log in endpoint
    def __init__(self):
        super(login, self).__init__()

    def post(self):

        username = request.form.get('username')
        user = manipulate.find_by_username(username)

        # verify password
        if not user or not user[1].verify_password(request.form.get('password')):
            return {
                'message': 'Invalid email or password, Please try again'
            }, 401
        access_token = user[1].generate_token(user[0]['id'], user[0]['isAdmin'])
        return {
            'message': 'You logged in successfully.',
            'access_token': access_token.decode()
        }, 200


class MyUser(Resource):
    def __init__(self):
        super(MyUser, self).__init__()
    
    # @token_required
    def get(self, id):
        result = manipulate.fetch_by_id(id)
        return {
            "status": 200,
            "data": [{"incidents": result, "message": "successfully fetched user record"}]
        }, 200

    # @token_required
    def put(self, id):
        data = edit_parser.parse_args()
        if not data:
            abort(400)
        manipulate.edit(id, data)      
        return {
            "status": 200,
            "data": [{"message": "successfully edited user record"}]
        }, 200