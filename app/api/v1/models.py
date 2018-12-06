from flask import Flask
from flask_restful import fields, reqparse
import datetime as dt
import uuid


incidents = [
    {
        "id": 1,
        "createdOn": dt.datetime.now,
        "createdBy": "Valerie Rono",
        "type_of_incident": "RedFlag",
        "location": "coordinates",
        "status": "pending",
        "images": "file path",
        "videos": "file path",
        "comment": "traffic police bribery"
    },
    {
        "id": 2,
        "createdOn": dt.datetime.now,
        "createdBy": "Valerie Rono",
        "type_of_incident": "RedFlag",
        "location": "coordinates",
        "status": "draft",
        "images": "file path",
        "videos": "file path",
        "comment": "traffic police bribery"
    }
]

class Incidents():
    def __init__(self, createdBy, type_of_incident, location, 
                    images, videos, comment):
        self.id = int(uuid.uuid1())
        self.createdOn = fields.DateTime()
        self.createdBy = createdBy
        self.type_of_incident = type_of_incident
        self.location = location
        self.status = "draft"
        self.images = images
        self.videos = videos
        self.comment = comment


record_parser = reqparse.RequestParser()
record_parser.add_argument('createdBy', required=True, help='please provide input', type=str, location='json')
record_parser.add_argument('type_of_incident', required=True, help='please provide input', type=str, default='', location='json')
record_parser.add_argument('location', required=True, help='please provide input', type=str, location='json')
record_parser.add_argument('images', required=True, help='please provide input', type=str, location='json')
record_parser.add_argument('videos', required=True, help='please provide input', type=str, default='', location='json')
record_parser.add_argument('comment', required=True, help='please comment', type=str, location='json')

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
    "uri": fields.Url('api-v1.incident')
}

