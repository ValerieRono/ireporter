from flask import Flask
from flask_restful import fields, reqparse, inputs
import datetime
import re

incidents = []

def generateId():
    if len(incidents) > 0:
        return incidents[-1]['id'] + 1
    return 1

class Incidents():
    def __init__(self, createdBy, type_of_incident, location, 
                    images, videos, comment):
        self.id = generateId()
        self.createdOn = datetime.datetime.now()
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

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('createdBy', type=str, location='json')
edit_parser.add_argument('type_of_incident', type=str, default='', location='json')
edit_parser.add_argument('location', type=str, location='json')
edit_parser.add_argument('images', type=str, location='json')
edit_parser.add_argument('videos', type=str, default='', location='json')
edit_parser.add_argument('comment', type=str, location='json')

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

