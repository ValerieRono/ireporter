from flask_restful import Resource, marshal

# local import
from app.api.v1.models import record_fields, incidents
from app.api.v1.models import record_parser, Incidents, edit_parser
from app.api.v2.utils import IncidentSchema

incident_Schema = IncidentSchema()
incidents_Schema = IncidentSchema(many=True)


class MyIncidents(Resource):

    def __init__(self):
        super(MyIncidents, self).__init__()
        self.parser = record_parser

    def get(self):
        if len(incidents) == 0:
            return {
                "status": 404,
                "data": [{"message": "no records found"}]
                }, 404
        result = [marshal(incident, record_fields) for incident in incidents]
        return {
            "status": 200,
            "data": [{"incidents": result, "message": "successfull"}]
            }, 200

    def post(self):
        args = self.parser.parse_args()
        keys = args.keys()
        for key in keys:
            if not args[key]:
                return {
                    "status": 400,
                    "data": [{"message": "bad request"}]
                    }, 400
        incident = Incidents(
            createdBy=args['createdBy'],
            type_of_incident=args['type_of_incident'],
            location=args['location'],
            images=args['images'],
            videos=args['videos'],
            comment=args['comment']
        )
        result = marshal(incident, record_fields)
        incidents.append(result)
        return {
            'status': 201,
            'data': [{"record": result, "message": "created record"}]
            }, 201

class MyIncident(Resource):

    def __init__(self):
        super(MyIncident, self).__init__()
        self.parser = record_parser

    def get(self, id):
        new_incidents = incidents_Schema.dump(incidents).data
        incident = [incident for incident in new_incidents if incident['id'] == id]

        if len(incident) == 0:
            return {
                "status": 404, 'data': [{"message": "record not found"}]
                }, 404
        result = marshal(incident[0], record_fields)
        return {
            "status": 200,
            "data": [{"incident": result, "message": "successfull"}]
            }, 200

    def put(self, id):
        new_incidents = incidents_Schema.dump(incidents).data
        incident = [incident for incident in new_incidents if incident['id'] == id]

        if len(incident) == 0:
            return {
                "status": 404,
                "data": [{"message": "record not found"}]
                }, 404
        incident_index = new_incidents.index(incident[0])

        if incident[0]['status'] != "draft":
            return {
                'status': 400,
                'data': [{"message": "cannot edit record"}]
                }, 400

        data = edit_parser.parse_args()
        for key in data.keys():
            if data[key]:
                incident[0][key] = data[key]        

        incidents[incident_index] = incident[0]
        return {
            'status': 200,
            'data': [{"record": incident[0], "message": "updated record"}]
            }, 200

    def delete(self, id):
        new_incidents = incidents_Schema.dump(incidents).data
        incident = [incident for incident in new_incidents if incident['id'] == id]

        if len(incident) == 0:
            return {
                "status": 404,
                "data": [{"message": "record not found"}]
                }, 404

        for item in incidents:
            if incident_Schema.dump(item).data == incident[0]:
                incidents.remove(item)
        result = marshal(incident[0], record_fields)

        return {
            'status': 200,
            'data': [{'record': result, "message": "deleted"}]
            }, 200