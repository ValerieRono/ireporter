# from flask import current_app
from flask_restful import fields, marshal
from datetime import datetime, timedelta
from passlib.apps import custom_app_context as pwd_context
import jwt

# local import
from app.database_config import init_db

class Users():

    """ user class """

    def __init__(self, firstname, lastname, othernames,
                 email, phoneNumber, username, password):
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.email = email
        self.phoneNumber = phoneNumber
        self.username = username
        self.password = password
        self.password_hash = pwd_context.encrypt(password)
        self.registered = datetime.now
        self.isAdmin = False

    def verify_password(self, password):

        """ verify password when user provides details during log in """

        return pwd_context.verify(password, self.password_hash)

    def generate_token(self, user_id, is_admin):

        """ Generates the access token"""
        SECRET_KEY = "g;ifdykrdsthawrxyg;fidkysktyrdyckrytkdG"

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=120),
                'iat': datetime.utcnow(),
                'user': {
                    'user_id': user_id,
                    'is_admin': is_admin
                }
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):

        """Decodes the access token from the Authorization header."""
        SECRET_KEY = "g;ifdykrdsthawrxyg;fidkysktyrdyckrytkdG"

        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload['user']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token."

class ManipulateDbase():
    def __init__(self):
        self.db = init_db()

    def fetch(self):
        # fetch data
        curr = self.db.cursor()
        query = """SELECT user_id, firstname, lastname, othernames,
                     username, email, phoneNumber, password,
                      registered, isAdmin FROM users_table"""
        curr.execute(query)
        data = curr.fetchall()
        response = []

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
                    FROM users_table WHERE user_id = {0}""".format(id)
        curr.execute(query)
        data = curr.fetchone()

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

    def find_by_username(self, username):
        query = """SELECT user_id, firstname, lastname,
                    othernames, username, email, phoneNumber, password,
                    registered, isAdmin FROM users_table WHERE username = '{0}'""".format(username)
        curr = self.db.cursor()
        curr.execute(query)
        data = curr.fetchone()
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
        return [user, email_user]

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

