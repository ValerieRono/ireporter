from flask import abort
from flask_restful import Resource, reqparse, marshal, inputs


# local import
from app.api.v2.incidents.models import Incidents, ManipulateDbase
from app.api.v2.incidents.models import record_fields

from app.api.v2.utils import token_required, IncidentSchema


record_parser = reqparse.RequestParser()

record_parser.add_argument(
    'type_of_incident',
    required=True,
    help='type can only be Redflag or Intervention',
    choices=('Redflag', 'Intervention'),
    location='json'
)

record_parser.add_argument(
    'location',
    required=True,
    help='wrong location format',
    type=inputs.regex('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$'),
    location='json'
    )

record_parser.add_argument(
    'images',
    required=True,
    help='Please provide input.',
    type=str,
    location='json'
    )
record_parser.add_argument(
    'videos',
    required=True,
    help='please provide input',
    type=str,
    location='json'
    )
record_parser.add_argument(
    'comment',
    required=True,
    help='please comment',
    type=inputs.regex('^[a-zA-Z\s*]{5,140}$'),
    location='json'
    )

edit_parser = reqparse.RequestParser()

edit_parser.add_argument(
    'type_of_incident',
    choices=('Redflag', 'Intervention'),
    help='type can only be Redflag or Intervention',
    location='json'
)
edit_parser.add_argument(
    'location',
    type=inputs.regex('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$'),
    location='json'
    )
edit_parser.add_argument(
    'images',
    type=list,
    location='json'
    )
edit_parser.add_argument(
    'videos',
    type=list,
    location='json'
    )
edit_parser.add_argument(
    'comment',
    type=inputs.regex('^[a-zA-Z]{5,140}$'),
    location='json'
    )
status_parser = reqparse.RequestParser()
status_parser.add_argument(
    'status',
    choices=('Under Investigation', 'Resolved', 'Rejected'),
    help='status can only be Under investigation, Resolved or Rejection',
    location='json'
)


incident_Schema = IncidentSchema()
incidents_Schema = IncidentSchema(many=True)


class MyIncidents(Resource):
    @token_required
    def get(self, user):
        if user['is_admin'] is True:
            response = ManipulateDbase().fetch()
            return {
                "status": 200,
                "data": [{"incidents": response, "message": "successfull"}]
            }, 200
        response = ManipulateDbase().fetch_all_own(id=user['user_id'])
        return {
            "status": 200,
            "data": [{"incidents": response, "message": "successfull"}]
        }, 200

    @token_required
    def post(self, user):
        data = record_parser.parse_args()
        keys = data.keys()
        for key in keys:
            if not data[key]:
                return {
                    "status": 404,
                    "data": [{"message": "please comment"}]
                }, 404
     
        incident = Incidents(
            createdBy=user['user_id'],
            type_of_incident=data['type_of_incident'],
            location=data['location'],
            images=data['images'],
            videos=data['videos'],
            comment=data['comment']
        )
        new_incident = incident_Schema.dump(incident).data
        save_incident = ManipulateDbase().save(new_incident)
        result = marshal(save_incident, record_fields)
        return {
            'status': 201,
            'data': [{"record": result, "message": "created incident record"}]
        }, 201


class MyIncident(Resource):
    def __init__(self):
        super(MyIncident, self).__init__()
        self.parser = record_parser

    @token_required
    def get(self, user, id):
        record = incident_Schema.dump(ManipulateDbase().fetchone(id)).data
        if record:
            if user['user_id'] == record['createdBy'] or user['is_admin'] is True:
                result = ManipulateDbase().fetchone(id)
                return {
                    "status": 200,
                    "data": [{"incidents": result, "message": "successfull"}]
                }, 200
            return {
                "status": 403,
                "message": "Forbidden, can only view record you created"
            }, 403
        return {
            "message": "incident not found"
        }, 404

    @token_required
    def put(self, user, id):
        record = incident_Schema.dump(ManipulateDbase().fetchone(id)).data
        # import pdb; pdb.set_trace()
        if record:
            if user['user_id'] == record['createdBy'] and record['status'] == 'draft': 
                data = edit_parser.parse_args()
                # pdb.set_trace()

                if not data:
                    return {
                        "message": "Invalid data provided"
                    }, 400
                ManipulateDbase().edit(id, data)      
                return {
                    "status": 200,
                    "data": [{
                        "message": "successfully edited record",
                        "record": record}]
                }, 200
            return {
                    "status": 403,
                    "message": "forbidden, cannot edit record"
            }, 403

        return {
            "status": 404,
            "message": "Record not found"
        }, 404

    @token_required
    def delete(self, user, id):
        record = incident_Schema.dump(ManipulateDbase().fetchone(id)).data
        if record:
            if user['user_id'] == record['createdBy'] or user['is_admin'] is True: 
                if record['status'] == "draft":
                    ManipulateDbase().delete(id)      
                    return {
                        "status": 200,
                        "data": [{"message": "successfully deleted record"}]
                    }, 200
                return {
                    "status": 403,
                    "message": "forbidden, can only delete record under draft"
                }, 403
            return {
                "status": 403,
                "message": "forbidden, can only delete own record"
            }, 403

        return {
            "status": 404,
            "message": "Record not found"
        }, 404

    @token_required
    def patch(self, user, id):
        data = status_parser.parse_args()
        if not data:
            abort(400)

        if user['is_admin'] is True:
            ManipulateDbase().edit(id, data)      
            return {
                "status": 200,
                "data": [{"message": "successfully edited record"}]
            }, 200
        return {
            "status": 403,
            "message": "Forbidden, cannot edit status"
        }, 403