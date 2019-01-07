# from flask import current_app
from datetime import datetime
from flask_restful import fields, marshal
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


# local import
from app.database_config import connection


class Users():

    """ user class """

    def __init__(self, **kwargs):
        self.firstname = kwargs.get("firstname")
        self.lastname = kwargs.get("lastname")
        self.othernames = kwargs.get("othernames")
        self.email = kwargs.get("email")
        self.phoneNumber = kwargs.get("phoneNumber")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.password_hash = generate_password_hash(self.password)
        self.registered = datetime.now
        self.isAdmin = False

    def verify_password(self, password):

        """ verify password when user provides details during log in """

        return check_password_hash(self.password_hash, password)

   
class ManipulateDbase():
    def __init__(self):
        db_url = current_app.config.get('DATABASE_URL')
        self.db = connection(url=db_url)

    def fetch(self):
        # fetch data
        curr = self.db.cursor()
        query = """SELECT user_id, firstname, lastname, othernames,
                     username, email, phoneNumber, password,
                      registered, isAdmin FROM users_table"""
        curr.execute(query)
        data = curr.fetchall()
        response = []
        if not data:
            return response

        for i, items in enumerate(data):
            user_id, firstname, lastname, othernames, username, email, phoneNumber, password, registered, isAdmin = items
            record = dict(
                id=user_id,
                firstname=firstname,
                lastname=lastname,
                othernames=othernames,
                username=username,
                email=email,
                phoneNumber=phoneNumber,
                password=password,
                registered=str(registered),
                isAdmin=isAdmin
            )
            result = marshal(record, record_fields)
            response.append(result)

        return response

    def fetch_by_id(self, id):
        # fetch data
        curr = self.db.cursor()
        query = """SELECT user_id, firstname, lastname,
                    othernames, username, email, phoneNumber,
                    password, registered, isAdmin
                    FROM users_table WHERE user_id = '{0}'""".format(id)
        curr.execute(query)
        data = curr.fetchone()
        if data is None:
            response = []
            return response
        user_id, firstname, lastname, othernames, username, email, phoneNumber, password, registered, isAdmin = data
        record = dict(
            id=user_id,
            firstname=firstname,
            lastname=lastname,
            othernames=othernames,
            username=username,
            email=email,
            phoneNumber=phoneNumber,
            password=password,
            registered=str(registered),
            isAdmin=isAdmin
        )
        result = marshal(record, record_fields)
        return result

    def find_by_username(self, identifier):
        query = """SELECT user_id, firstname, lastname,
                    othernames, username, email, phoneNumber, password,
                    registered, isAdmin FROM users_table WHERE username = '{0}'""".format(identifier)
        curr = self.db.cursor()
        curr.execute(query)
        data = curr.fetchone()
        if data is None:
            response = []
            return response
        user_id, firstname, lastname, othernames, username, email, phoneNumber, password, registered, isAdmin = data
        user = dict(
            id=user_id,
            firstname=firstname,
            lastname=lastname,
            othernames=othernames,
            username=username,
            email=email,
            phoneNumber=phoneNumber,
            password=password,
            registered=str(registered),
            isAdmin=isAdmin
        )
        email_user = Users(
            firstname=user['firstname'],
            lastname=user['lastname'],
            othernames=user['othernames'],
            username=user['othernames'],
            email=user['email'],
            phoneNumber=user['phoneNumber'],
            password=user['password']
            )
        response = [user, email_user]
        return response

    def save(self, record_to_add):
        # save data
        query = """INSERT INTO users_table
                    (firstname, lastname, othernames,
                    username, email, phoneNumber, password, isAdmin)
                    VALUES (%(firstname)s, %(lastname)s, %(othernames)s,
                    %(username)s, %(email)s, %(phoneNumber)s, %(password)s,
                    %(isAdmin)s) RETURNING user_id;"""
        curr = self.db.cursor()
        curr.execute(query, record_to_add)
        value = curr.fetchone()
        self.db.commit()
       
        return self.fetch_by_id(value[0])

    def edit(self, id, data_to_edit):
        for key in data_to_edit.keys():
            if data_to_edit[key]:
                curr = self.db.cursor()
                curr.execute(
                    """UPDATE users_table SET {0} = '{1}'
                    WHERE user_id = '{2}'""".format(key, data_to_edit[key], id,)
                )
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

