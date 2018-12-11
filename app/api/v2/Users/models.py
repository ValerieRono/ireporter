from flask_restful import fields, marshal
import datetime

# local import
from app.database_config import init_db

class Users():
    def __init__(self, firstname, lastname, othernames,
                 email, phoneNumber, username, password_hash):
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.email = email
        self.phoneNumber = phoneNumber
        self.username = username
        self.password_hash = password_hash
        self.registered = datetime.datetime.now
        self.isAdmin = False

class ManipulateDbase():
    def __init__(self):
        self.db = init_db()

    def fetch(self):
        # fetch data
        curr = self.db.cursor()
        query = """SELECT user_id, firstname, lastname, othernames,
                     username, email, phoneNumber, password_hash,
                      registered, isAdmin FROM users_table"""
        curr.execute(query)
        data = curr.fetchall()
        response = []

        for i, items in enumerate(data):
            user_id, firstname, lastname, othernames, username, email, phoneNumber, password_hash, registered, isAdmin = items
            record = dict(
                id=user_id,
                firstname=firstname,
                lastname=lastname,
                othernames=othernames,
                username=username,
                email=email,
                phoneNumber=phoneNumber,
                password=password_hash,
                registered=str(registered),
                isAdmin=isAdmin
            )
            result = marshal(record, record_fields)
            response.append(result)

        return response

    def fetch_by_id(self, id):
        # fetch data
        curr = self.db.cursor()
        query = """SELECT user_id, firstname, lastname, othernames, username, email, phoneNumber, password_hash, registered, isAdmin FROM users_table WHERE user_id = {0}""".format(id)
        curr.execute(query)
        data = curr.fetchone()

        user_id, firstname, lastname, othernames, username, email, phoneNumber, password_hash, registered, isAdmin = data
        record = dict(
            id=user_id,
            firstname=firstname,
            lastname=lastname,
            othernames=othernames,
            username=username,
            email=email,
            phoneNumber=phoneNumber,
            password=password_hash,
            registered=str(registered),
            isAdmin=isAdmin
        )
        result = marshal(record, record_fields)
        return result

    def save(self, record_to_add):
        # save data
        query = """ INSERT INTO users_table (firstname, lastname, othernames, username, email, phoneNumber, password_hash, isAdmin) 
                    VALUES (%(firstname)s, %(lastname)s, %(othernames)s, %(username)s, %(email)s, %(phoneNumber)s, %(password_hash)s, %(isAdmin)s) RETURNING user_id;"""
        curr = self.db.cursor()
        curr.execute(query, record_to_add)
        value = curr.fetchone()
        self.db.commit()

        return self.fetch_by_id(value[0])

    def edit(self, id, data_to_edit):
        for key in data_to_edit.keys():
            if data_to_edit[key]:
                curr = self.db.cursor()
                curr.execute("""UPDATE users_table SET {0} = '{1}' WHERE user_id = '{2}'""".format(key, data_to_edit[key], id, ))
                self.db.commit()

    def delete(self, id):
        curr = self.db.cursor() 
        curr.execute("""DELETE FROM users_table WHERE user_id = %s""", (id,))
        self.db.commit()

record_fields = {
    "id": fields.Integer,
    "firstname": fields.String,
    "lastname": fields.String,
    "othernames": fields.String,
    "email": fields.String,
    "phoneNumber": fields.String,
    "username": fields.String, 
    "registered": fields.String,
    "isAdmin": fields.Boolean,
    "uri": fields.Url('api-v2.user')
}
