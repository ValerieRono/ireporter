from flask import abort
from flask import request
from flask_restful import Resource, reqparse, marshal, inputs
from marshmallow import Schema, fields


# local import
from app.api.v2.Users.models import record_fields, Users, ManipulateDbase
from app.api.v2.utils import generate_token, decode_token
from app.api.v2.utils import token_required

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

login_parser = reqparse.RequestParser()

login_parser.add_argument(
    'username',
    type=str,
    location='json'
)
login_parser.add_argument(
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


class MyUsers(Resource):
    def __init__(self):
        super(MyUsers, self).__init__()
        self.parser = record_parser
    
    @token_required
    def get(self, user):
        if user['is_admin'] is True:
            response = ManipulateDbase().fetch()
            return {
                "status": 200,
                "data": [{"incidents": response, "message": "successfull"}]
            }, 200
        return {
            "status": 403,
            "message": "Forbidden, only admin can view all users"
        }, 403

    def post(self):
        args = self.parser.parse_args()
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
        save_user = ManipulateDbase().save(new_user)
        result = marshal(save_user, record_fields)
        return {
            'status': 201,
            'data': [{"user": result, "message": "registered user"}]
        }, 201


class login(Resource):
    # log in endpoint
    def __init__(self):
        super(login, self).__init__()

    def post(self):

        data = login_parser.parse_args()
        username = data['username']
        user = ManipulateDbase().find_by_username(username)
        # import pdb; pdb.set_trace()
        # verify password
        if not user or not user[1].verify_password(data['password']):
            return {
                'message': 'Invalid email or password, Please try again'
            }, 401
        access_token = generate_token(self, user[0]['id'], user[0]['isAdmin'])
        return {
            'message': 'You logged in successfully.',
            'access_token': access_token.decode()
        }, 200


class MyUser(Resource):
    def __init__(self):
        super(MyUser, self).__init__()
    
    @token_required
    def get(self, user, id):
        if user['user_id'] == id or user['isAdmin'] is True:
            result = ManipulateDbase().fetch_by_id(id)
            return {
                "status": 200,
                "data": [{"incidents": result, "message": "successfull"}]
            }, 200
        return {
            "status": 403,
            "message": "Forbidden, can only view own record"
        }, 403

    # @token_required
    def put(self, user, id):
        if user['user_id'] == id:
            data = edit_parser.parse_args()
            if not data:
                abort(400)
            ManipulateDbase().edit(id, data)      
            return {
                "status": 200,
                "data": [{"message": "successfully edited user record"}]
            }, 200
        return {
            "status": 403,
            "message": "Forbidden, can only edit own record"
        }, 403