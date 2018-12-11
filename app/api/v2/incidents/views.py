from flask import Flask, json, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, marshal, inputs
from marshmallow import Schema, fields
import re

# local import
from app.api.v2.incidents.models import Incidents, ManipulateDbase, record_fields

record_parser = reqparse.RequestParser()
record_parser.add_argument('createdBy', required=True, help='please provide input', type=int, location='json')
record_parser.add_argument('type_of_incident', required=True, help='type can only be Redflag or Intervention', type=inputs.regex(r'^\b(Redflag|intervention)\b$'), default='', location='json')
record_parser.add_argument('location', required=True, help='please provide input', type=str, location='json')
record_parser.add_argument('images', required=True, help='please provide input', type=str, location='json')
record_parser.add_argument('videos', required=True, help='please provide input', type=str, default='', location='json')
record_parser.add_argument('comment', required=True, help='please comment', type=inputs.regex(r'^(?!\s*$).+'), location='json')

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('createdBy', type=int, location='json')
edit_parser.add_argument('type_of_incident', type=str, default='', location='json')
edit_parser.add_argument('location', type=str, location='json')
edit_parser.add_argument('images', type=str, location='json')
edit_parser.add_argument('videos', type=str, default='', location='json')
edit_parser.add_argument('comment', type=str, location='json')



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


incident_Schema = IncidentSchema()
incidents_Schema = IncidentSchema(many=True)


class MyIncidents(Resource):
    def __init__(self):
        super(MyIncidents, self).__init__()
        self.parser = record_parser
        self.manipulate = ManipulateDbase()
       

    def get(self):
        response = self.manipulate.fetch()
        return {"status": 200, "data": [{"incidents": response, "message": "successfully fetched all records"}]}, 200

    def post(self):
        args = self.parser.parse_args()
        keys = args.keys()
        for key in keys:
            if not args[key]:
                return {"status": 404, "data": [{"message": "please comment on the incident you would like to report"}]}, 404
        incident = Incidents(
            createdBy=args['createdBy'],
            type_of_incident=args['type_of_incident'],
            location=args['location'],
            images=args['images'],
            videos=args['videos'],
            comment=args['comment']
        )
        new_incident = incident_Schema.dump(incident).data
        self.manipulate.save(new_incident)
        return {'status': 201, 'data': [{"record": marshal(incident, record_fields), "message": "created red flag record"}]}, 201


class MyIncident(Resource):
    def __init__(self):
        super(MyIncident, self).__init__()
        self.parser = record_parser
        self.manipulate = ManipulateDbase()
        
    def get(self, id):
        result = self.manipulate.fetchone(id)
        return {"status": 200, "data": [{"incidents": result, "message": "successfully fetched record"}]}, 200

    def put(self, id):
        data = edit_parser.parse_args()
        if not data:
            abort(400)
        self.manipulate.edit(id, data)      
        return {"status": 200, "data": [{"message": "successfully edited record"}]}, 200

    def delete(self, id):
        self.manipulate.delete(id)
        return {"status": 200, "data": [{"message": "successfully deleted record"}]}, 200