from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, fields

#local import
from models import Incident, IncidentSchema, incident_list

incident_Schema = IncidentSchema()
incidents_Schema = IncidentSchema(many=True)

class MyIncidents(Resource):
    def __init__(self):
        super(MyIncidents, self).__init__()

    def get(self):
        incidents = incidents_Schema.dump(incident_list).data
        return {"status":"success", "data":incidents}, 200