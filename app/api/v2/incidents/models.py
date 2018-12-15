from flask_restful import fields, marshal
import datetime

from app.database_config import init_db


class Incidents():
    def __init__(self, createdBy, type_of_incident, location,
                 images, videos, comment):
        self.createdOn = datetime.datetime.now()
        self.createdBy = createdBy
        self.type_of_incident = type_of_incident
        self.location = location
        self.status = "draft"
        self.images = images
        self.videos = videos
        self.comment = comment


class ManipulateDbase():
    def __init__(self):
        self.db = init_db()

    def fetch(self):
        # fetch data
        curr = self.db.cursor()
        query = """SELECT incidents_id, createdOn, createdBy,
                    type_of_incident, status, comment, location,
                    images, videos FROM incidents"""
        curr.execute(query)
        data = curr.fetchall()
        response = []
        
        for i, items in enumerate(data):
            incidents_id, createdOn, createdBy, type_of_incident, status, comment, location, images, videos = items
            record = dict(
                id=incidents_id,
                createdOn=str(createdOn),
                createdBy=createdBy,
                type_of_incident=type_of_incident,
                status=status,
                comment=comment,
                location=location,
                images=images,
                videos=videos
            )
            result = marshal(record, record_fields)
            response.append(result)

        return response

    def fetch_all_own(self, id):
        # fetch data
        curr = self.db.cursor()
        query = """SELECT incidents_id, createdOn, createdBy,
                    type_of_incident, status, comment, location,
                    images, videos FROM incidents WHERE createdBy = '{0}'""".format(id)
        curr.execute(query)
        data = curr.fetchall()
        response = []
        
        for i, items in enumerate(data):
            incidents_id, createdOn, createdBy, type_of_incident, status, comment, location, images, videos = items
            record = dict(
                id=incidents_id,
                createdOn=str(createdOn),
                createdBy=createdBy,
                type_of_incident=type_of_incident,
                status=status,
                comment=comment,
                location=location,
                images=images,
                videos=videos
            )
            result = marshal(record, record_fields)
            response.append(result)

        return response

    def fetchone(self, id):
        # fetch data
        curr = self.db.cursor()
        query = """SELECT incidents_id, createdOn, createdBy,
                    type_of_incident, status, comment, location,
                    images, videos FROM incidents WHERE incidents_id = {0}""".format(id)
        curr.execute(query)
        data = curr.fetchone()
    
        incidents_id, createdOn, createdBy, type_of_incident, status, comment, location, images, videos = data
        record = dict(
            id=incidents_id,
            createdOn=str(createdOn),
            createdBy=createdBy,
            type_of_incident=type_of_incident,
            status=status,
            comment=comment,
            location=location,
            images=images,
            videos=videos
        )
        result = marshal(record, record_fields)
        return result

    def save(self, record_to_add):
        # save data
        query = """INSERT INTO incidents
                    (createdBy, type_of_incident,
                    status, comment, location, images, videos) 
                    VALUES (%(createdBy)s, %(type_of_incident)s,
                    %(status)s, %(comment)s, %(location)s, %(images)s,
                    %(videos)s) RETURNING incidents_id;"""

        curr = self.db.cursor()
        curr.execute(query, record_to_add)
        value = curr.fetchone()
        self.db.commit()
       
        return self.fetchone(value[0])

    def edit(self, id, data_to_edit):
        for key in data_to_edit.keys():
            if data_to_edit[key]:
                curr = self.db.cursor()
                curr.execute(
                    """UPDATE incidents SET {0} = '{1}' WHERE incidents_id = '{2}'""".format(key, data_to_edit[key], id, )
                )
                self.db.commit()

    def delete(self, id):
        curr = self.db.cursor() 
        curr.execute(
            """DELETE FROM incidents WHERE incidents_id = %s""", (id,)
        )
        self.db.commit()
        
    
record_fields = {
    "id": fields.Integer,
    "createdOn": fields.String,
    "createdBy": fields.Integer,
    "type_of_incident": fields.String,
    "location": fields.String,
    "status": fields.String,
    "images": fields.String,
    "videos": fields.String,
    "comment": fields.String,
    "uri": fields.Url('api-v2.new_incident')
}

