from flask import Flask, json, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, marshal
from marshmallow import Schema, fields

# local import
from app.api.v1.models import record_fields, incidents, record_parser, Incidents

#for serialization 
class IncidentSchema(Schema):
    id = fields.Int()
    createdOn = fields.DateTime()
    createdBy = fields.Str()
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

    def get(self):
        result = [marshal(incident, record_fields) for incident in incidents]
        return {"status": 200, "data": [{"incidents": result, "message": "successfully fetched all records"}]}, 200
        

    def post(self):
        args = self.parser.parse_args()
        keys = args.keys()
        for key in keys:
            if not args[key]:
                return {"status": 404, "data": [{"message": "please comment on the incident you would like to report"}]}, 404
        incident = Incidents(
            createdBy = args['createdBy'],
            type_of_incident = args['type_of_incident'],
            location = args['location'],
            images = args['images'],
            videos = args['videos'],
            comment = args['comment']
        )
        incidents.append(incident)
        return {'status': 201, 'data': [{"record": marshal(incident, record_fields), "message": "created red flag record"}]}, 201
        


class MyIncident(Resource):
    def __init__(self):
        super(MyIncident, self).__init__()
        self.parser = record_parser

    def get(self, id):
        new_incidents = incidents_Schema.dump(incidents).data
        incident = [incident for incident in new_incidents if incident['id'] == id]
        if len(incident) == 0:
            abort(404)
        return {
            'status': 200,
            'data': marshal(incident[0], record_fields)
        }

    def put(self, id):
        new_incidents = incidents_Schema.dump(incidents).data
        for incident in new_incidents:
            if incident['id'] == id:
                new_incident = incident
                if new_incident['status'] != "draft":
                    return {'status': 404, 'data': [{"message": "cannot edit record"}]}, 404

        if len(new_incident) == 0:
            abort(404)
        args = self.parser.parse_args()
        if not args:
            abort(400)
        for key in args.keys():
            if args[key] in args and type(key) != unicode:
                abort(400)
            if args[key] is not None:
                new_incident[key] = args[key]
        for item in incidents:
            if incident_Schema.dump(item).data == new_incident:
                updated_incident = incident_Schema.load(new_incident).data
                item == updated_incident
        return {'status': 200, 'data': [{'record': marshal(new_incident, record_fields), "message": "updated red flag record"}]}, 200

    def delete(self, id):
        new_incidents = incidents_Schema.dump(incidents).data
        for incident in new_incidents:
            if incident['id'] == id:
                new_incident = incident
        if len(new_incident) == 0:
            abort(404)
        for item in incidents:
            if incident_Schema.dump(item).data == new_incident:
                incidents.remove(item)
        return {'status': 200, 'data': [{'record': marshal(new_incident, record_fields), "message": "deleted a red flag record"}]}, 200
        
       
        
        
