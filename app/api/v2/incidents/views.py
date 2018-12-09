from flask import Flask, json, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, marshal
from marshmallow import Schema, fields

# local import
from app.api.v2.incidents.models import record_fields, record_parser, Incidents, edit_parser

from app.database_config import init_db

# for serialization
class IncidentSchema(Schema):
    id = fields.Int()
    createdBy = fields.Str()
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
    def __init__(self):
        super(MyIncidents, self).__init__()
        self.parser = record_parser
        self.db = init_db()

    def get(self):
        #fetch data
        curr = self.db.cursor()
        query = """SELECT incidents_id, createdOn, createdBy, type_of_incident, status, comment, location, images, videos FROM incidents"""
        curr.execute(query)
        data = curr.fetchall()
        response = []
        
        for i, items in enumerate(data):
            incidents_id, createdOn, createdBy, type_of_incident, status, comment, location, images, videos = items
            record = dict (
                id = int(incidents_id),
                createdOn = str(createdOn),
                createdBy = createdBy,
                type_of_incident = type_of_incident,
                status = status,
                comment = comment,
                location = location,
                images = images,
                videos = videos
            )
            result = marshal(record, record_fields)
            response.append(result)

        return {"status": 200, "data": [{"incidents": response, "message": "successfully fetched all records"}]}, 200

    def post(self):
        args = self.parser.parse_args()
        keys = args.keys()
        for key in keys:
            if not args[key]:
                return {"status": 404, "data": [{"message": "please comment on the incident you would like to report"}]}, 404
        incident = Incidents(
            createdBy=args['createdBy'],
            type_of_incident=args['type_of_incident'],
            location=args['location'],
            images=args['images'],
            videos=args['videos'],
            comment=args['comment']
        )
        new_incident = incident_Schema.dump(incident).data
        query = """INSERT INTO incidents (incidents_id, createdBy, type_of_incident, status, comment, location, images, videos) 
                    VALUES (%(id)s, %(createdBy)s, %(type_of_incident)s, %(status)s, %(comment)s, %(location)s, %(images)s, %(videos)s);"""
        curr = self.db.cursor()
        curr.execute(query, new_incident)
        self.db.commit()
        return {'status': 201, 'data': [{"record": marshal(incident, record_fields), "message": "created red flag record"}]}, 201


class MyIncident(Resource):
    def __init__(self):
        super(MyIncident, self).__init__()
        self.parser = record_parser
        self.db = init_db()

    def get(self, id):
        #fetch data
        curr = self.db.cursor()
        query = """SELECT incidents_id, createdOn, createdBy, type_of_incident, status, comment, location, images, videos FROM incidents WHERE incidents_id = {0}""".format(id)
        curr.execute(query)
        data = curr.fetchone()
    
        incidents_id, createdOn, createdBy, type_of_incident, status, comment, location, images, videos = data
        record = dict (
            id = int(incidents_id),
            createdOn = str(createdOn),
            createdBy = createdBy,
            type_of_incident = type_of_incident,
            status = status,
            comment = comment,
            location = location,
            images = images,
            videos = videos
        )
        result = marshal(record, record_fields)
        return {"status": 200, "data": [{"incidents": result, "message": "successfully fetched record"}]}, 200

    def put(self, id):
        data = edit_parser.parse_args()
        #import pdb; pdb.set_trace()
        if not data:
            abort(400)
        for key in data.keys():
            if data[key]:
                curr = self.db.cursor()
                #import pdb; pdb.set_trace()
                curr.execute("""UPDATE incidents SET {0} = '{1}' WHERE incidents_id = '{2}'""".format(key, data[key], id, ))
                #import pdb; pdb.set_trace()
                self.db.commit()

        return {"status": 200, "data": [{"message": "successfully edited record"}]}, 200

    def delete(self, id):
        curr = self.db.cursor() 
        curr.execute("""DELETE FROM incidents WHERE incidents_id = %s""", (id,))
        self.db.commit()
        
        return {"status": 200, "data": [{"message": "successfully deleted record"}]}, 200