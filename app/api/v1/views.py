from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, fields

#local import
from app.api.v1.models import Incident, IncidentSchema, incident_list

incident_Schema = IncidentSchema()
incidents_Schema = IncidentSchema(many=True)

class MyIncidents(Resource):
    def __init__(self):
        super(MyIncidents, self).__init__()

    def get(self):
        incidents = incidents_Schema.dump(incident_list).data
        return jsonify({"status": 200, "data": [{"incidents": incidents, "message" : "successfully fetched all records"}]})
    
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'status':200, 'message': 'no input data provided'}, 404
        # Validate and deserialize input 
        data, errors = incident_Schema.dump(json_data)
        if errors:
            return {"status": 422, "data": errors}, 422
        elif not data['comment']:
            return {"status": 404, "data": [{"message" : "please comment on the incident you would like to report"}]}, 404
        new_incident = Incident(
            createdBy = data['createdBy'],
            type_of_incident = data['type_of_incident'],
            location = data['location'],
            images = data['images'],
            videos = data['videos'],
            comment = data['comment']
            )
        
        incident_list.append(new_incident)
        result = incident_Schema.dump(new_incident).data

        #message = {
        #   'status': 201,
        #    "data" : [{
        #        "id" : result['id'],
        #        "message" : "created red flag record"
        #    }
        #    ]
        #    
        #}
        #resp = jsonify(message)
        #resp.status_code = 201

        #return resp
        return {'status': 201, 'data': [{"record" : result, "message": "created red flag record"}]}, 201
        #return jsonify({'status': 200, 'data': [{"id" : result['id'], "message" : "created red flag record"}]})
        

class MyIncident(Resource):
    def __init__(self):
        super(MyIncident, self).__init__()

    def get(self, id):
        incidents = incidents_Schema.dump(incident_list).data
        for incident in incidents:
            if incident['id'] == id:
                incidents = incidents_Schema.dump(incident_list).data
                incident = [incident for incident in incidents if incident['id'] == id]
                return jsonify({"status": 200, "data": [incident]})

        return {'status': 404, 'data': [{"message" : "red flag record not found"}]}, 404
    

    def put(self, id):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'status':404, 'message': 'no input data provided'}, 404
        # Validate and deserialize input
        data = incident_Schema.dump(json_data).data
        incidents = incidents_Schema.dump(incident_list).data
        for incident in incidents:
            if incident['id'] == id:
                if incident['status'] != "draft":
                    return {'status': 404, 'data': [{"message" : "cannot edit record"}]}, 404
        
                for key in data.keys():
                    if data[key] is not None:
                        incident[key] = data[key] 

                    updated_incident = incident_Schema.load(incident).data
                    incident_list[id-1] = updated_incident

                    result = incident_Schema.dump(incident).data
        
        
        

        return jsonify({'status': 200, 'data': [{"record" : result, "message" : "updated red flag record" }]})

    def delete(self, id):
        incidents = incidents_Schema.dump(incident_list).data
        for incident in incidents:
            if incident['id'] == id:
                incident = incident_list[id-1]
                incident_list.remove(incident)
        
                result = incident_Schema.dump(incident).data

        
                return jsonify({"Status": 200, "data": [{"id" : result['id'], "message" : "deleted a red flag record" }]})
            
        return {'status': 404, 'data': [{"message" : "red flag record not found"}]}, 404
        
        
        
        #return {'status': 204, 'data': [{"id" : result['id'], "message" : "deleted red flag record"}]},204