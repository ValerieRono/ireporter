from flask_restful import fields, reqparse, inputs
import datetime

incidents = []


def generateId():
    if len(incidents) > 0:
        return incidents[-1]['id'] + 1
    return 1


class Incidents():
    def __init__(self, **kwargs):
        self.id = generateId()
        self.createdOn = datetime.datetime.now()
        self.createdBy = kwargs.get("createdBy")
        self.type_of_incident = kwargs.get("type_of_incident")
        self.location = kwargs.get("location")
        self.status = "draft"
        self.images = kwargs.get("images")
        self.videos = kwargs.get("videos")
        self.comment = kwargs.get("comment")


record_parser = reqparse.RequestParser()

record_parser.add_argument(
    'createdBy', required=True, help='provide input', type=str, location='json'
    )
record_parser.add_argument(
    'type_of_incident', required=True,
    help='can only be Redflag or Intervention',
    type=inputs.regex(r'^\b(Redflag|Intervention)\b$'), location='json'
    )
record_parser.add_argument(
    'location', required=True, help='provide input', type=str, location='json'
    )
record_parser.add_argument(
    'images', required=True, help='provide input', type=str, location='json'
    )
record_parser.add_argument(
    'videos', required=True, help='provide input', type=str, location='json'
    )
record_parser.add_argument(
    'comment', required=True, help='please comment', type=str, location='json'
    )

edit_parser = reqparse.RequestParser()

edit_parser.add_argument(
    'createdBy', type=str, location='json'
    )
edit_parser.add_argument(
    'type_of_incident',
    type=inputs.regex(r'^\b(Redflag|Intervention)\b$'), location='json'
    )
edit_parser.add_argument(
    'location', type=str, location='json'
    )
edit_parser.add_argument(
    'images', type=str, location='json'
    )
edit_parser.add_argument(
    'videos', type=str, default='', location='json'
    )
edit_parser.add_argument(
    'comment', type=str, location='json'
    )

record_fields = {
    "id": fields.Integer,
    "createdOn": fields.String,
    "createdBy": fields.String,
    "type_of_incident": fields.String,
    "location": fields.String,
    "status": fields.String,
    "images": fields.String,
    "videos": fields.String,
    "comment": fields.String,
    "uri": fields.Url('api-v1.myincident')
}

