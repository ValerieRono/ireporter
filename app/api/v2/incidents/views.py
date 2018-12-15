from flask import abort
from flask_restful import Resource, reqparse, marshal, inputs
from marshmallow import Schema, fields

# local import
from app.api.v2.incidents.models import Incidents, ManipulateDbase
from app.api.v2.incidents.models import record_fields

from app.api.v2.utils import token_required


record_parser = reqparse.RequestParser()

record_parser.add_argument(
    'type_of_incident',
    required=True,
    help='type can only be Redflag or Intervention',
    type=inputs.regex(r'^\b(Redflag|intervention)\b$'), 
    location='json'
)

record_parser.add_argument(
    'location',
    required=True,
    help='please provide input',
    type=str,
    location='json'
    )

record_parser.add_argument(
    'images',
    required=True,
    help='please provide input',
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
    type=inputs.regex(r'^(?!\s*$).+'),
    location='json'
    )

edit_parser = reqparse.RequestParser()
# edit_parser.add_argument(
#     'createdBy',
#     type=int,
#     location='json'
#     )
edit_parser.add_argument(
    'type_of_incident',
    type=str,
    location='json'
    )
edit_parser.add_argument(
    'location',
    type=str,
    location='json'
    )
edit_parser.add_argument(
    'images',
    type=str,
    location='json'
    )
edit_parser.add_argument(
    'videos',
    type=str,
    location='json'
    )
edit_parser.add_argument(
    'comment',
    type=str,
    location='json'
    )
status_parser = reqparse.RequestParser()
status_parser.add_argument(
    'status',
    type=inputs.regex(r'^\b(Under Investigation|Rejected|Resolved)\b$'),
    location='json'
)


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
    @token_required
    def get(self, user):
        if user['is_admin'] is True:
            response = ManipulateDbase().fetch()
            return {
                "status": 200,
                "data": [{"incidents": response, "message": "successfull"}]
            }, 200
        response = ManipulateDbase().fetch_all_own(user['user_id'])
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
        if user['user_id'] == record['createdBy'] or user['isAdmin'] is True:
            result = ManipulateDbase().fetchone(id)
            return {
                "status": 200,
                "data": [{"incidents": result, "message": "successfull"}]
            }, 200
        return {
            "status": 403,
            "message": "Forbidden, can only view record you created"
        }, 403

    @token_required
    def put(self, user, id):
        record = incident_Schema.dump(ManipulateDbase().fetchone(id)).data
        if user['user_id'] == record['createdBy'] and record['status'] == 'draft': 
            data = edit_parser.parse_args()
            if not data:
                abort(400)
            ManipulateDbase().edit(id, data)      
            return {
                "status": 200,
                "data": [{"message": "successfully edited record"}]
            }, 200
        return {
                "status": 403,
                "message": "forbidden, cannot edit record"
        }, 403

    @token_required
    def delete(self, user, id):
        record = incident_Schema.dump(ManipulateDbase().fetchone(id)).data
        if user['user_id'] == record['createdBy'] or user['isAdmin'] is True: 
            return {
                "status": 200,
                "data": [{"message": "successfully deleted record"}]
            }, 200
        return {
            "status": 403,
            "message": "forbidden, can only delete own record"
        }, 403

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