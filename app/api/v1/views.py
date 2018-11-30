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
    
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = incident_Schema.dump(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        new_incident = Incident(
            createdBy = data['createdBy'],
            type_of_incident = data['type_of_incident'],
            location = data['location'],
            status = data['status'],
            images = data['images'],
            videos = data['videos'],
            comment = data['comment']
            )
        
        incident_list.append(new_incident)
        result = incident_Schema.dump(new_incident).data

        return {'status': "success", 'data': result}, 201