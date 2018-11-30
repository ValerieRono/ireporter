from marshmallow import Schema, fields
import datetime as dt


#incident list
incident_list = [
    {
        "id": 1,
        "createdOn" : dt.datetime.now,  
        "createdBy" : "Valerie Rono", 
        "type_of_incident" : "RedFlag",
        "location" : "coordinates",
        "status": "pending",
        "images" : "file path", 
        "videos" : "file path",
        "comment" : "traffic police bribery"
    },
    {
        "id": 2,
        "createdOn" : dt.datetime.now,  
        "createdBy" : "Valerie Rono", 
        "type_of_incident" : "RedFlag",
        "location" : "coordinates",
        "status": "pending",
        "images" : "file path", 
        "videos" : "file path",
        "comment" : "traffic police bribery"
    }
]

#basic incident model
class Incident(object):
    def __init__(self, createdBy, type_of_incident, location, status, images, videos, comment):
        self.id = len(incident_list) + 1
        self.createdOn = dt.datetime.now
        self.createdBy = createdBy
        self.type_of_incident = type_of_incident
        self.location = location
        self.status = status
        self.images = images
        self.videos = videos
        self.comment = comment

    def __repr__(self):
        return '<Incident(comment={self.comment!r})>'.format(self=self)


#create schema
class IncidentSchema(Schema):
    id = fields.Int()
    createdOn = fields.DateTime()
    createdBy = fields.Str()
    type_of_incident = fields.Str()
    location = fields.Str()
    status = fields.Str()
    images = fields.Str()
    videos = fields.Str()
    comment = fields.Str(required=True, help=("please comment on the incident you would like to report"))


