from flask import Flask, json, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, marshal, inputs
from marshmallow import Schema, fields
import re

# local import
from app.api.v2.Users.models import record_fields, Users, ManipulateDbase

record_parser = reqparse.RequestParser()
record_parser.add_argument('firstname', required=True, help='please provide input', type=str, location='json')
record_parser.add_argument('lastname', required=True, help='please provide input', type=str, default='', location='json')
record_parser.add_argument('othernames', required=True, help='please provide input', type=str, location='json')
record_parser.add_argument('email', required=True, help='please provide input', type=str, location='json')
record_parser.add_argument('phoneNumber', required=True, help='please provide input', type=str, default='', location='json')
record_parser.add_argument('username', required=True, help='please comment', type=str, location='json')
record_parser.add_argument('password_hash', required=True, help='password required', type=str, location='json')

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('firstname', type=str, location='json')
edit_parser.add_argument('lastname', type=str, default='', location='json')
edit_parser.add_argument('othernames', type=str, location='json')
edit_parser.add_argument('email', type=str, location='json')
edit_parser.add_argument('phoneNumber', type=str, default='', location='json')
edit_parser.add_argument('username', type=str, location='json')
edit_parser.add_argument('password_hash', required=True, help='password required', type=str, location='json')

# for serialization
class IncidentSchema(Schema):
    id = fields.Int()
    firstname = fields.Str()
    lastname = fields.Str()
    othernames = fields.Str()
    email = fields.Str()
    phoneNumber = fields.Str()
    username = fields.Str()
    password_hash = fields.Str()
    registered = fields.DateTime()
    isAdmin = fields.Boolean()


incident_Schema = IncidentSchema()
incidents_Schema = IncidentSchema(many=True)


class MyUsers(Resource):
    def __init__(self):
        super(MyUsers, self).__init__()
        self.parser = record_parser
        self.manipulate = ManipulateDbase()
       

    def get(self):
        response = self.manipulate.fetch()
        return {"status": 200, "data": [{"incidents": response, "message": "successfully fetched all user records"}]}, 200

    def post(self):
        args = self.parser.parse_args()
        keys = args.keys()
        for key in keys:
            if not args[key]:
                return {"status": 404, "data": [{"message": "please provide input"}]}, 404
        user = Users(
            firstname=args['firstname'],
            lastname=args['lastname'],
            othernames=args['othernames'],
            email=args['email'],
            phoneNumber=args['phoneNumber'],
            username=args['username'],
            password_hash=args['password_hash']
        )
        new_user = incident_Schema.dump(user).data
        result = self.manipulate.save(new_user)
        return {'status': 201, 'data': [{"record": marshal(result, record_fields), "message": "registered user"}]}, 201


class MyUser(Resource):
    def __init__(self):
        super(MyUser, self).__init__()
        self.parser = record_parser
        self.manipulate = ManipulateDbase()
        
    def get(self, id):
        result = self.manipulate.fetch_by_id(id)
        return {"status": 200, "data": [{"incidents": result, "message": "successfully fetched user record"}]}, 200

    def put(self, id):
        data = edit_parser.parse_args()
        if not data:
            abort(400)
        self.manipulate.edit(id, data)      
        return {"status": 200, "data": [{"message": "successfully edited user record"}]}, 200

    def delete(self, id):
        self.manipulate.delete(id)
        return {"status": 200, "data": [{"message": "successfully deleted user record"}]}, 200