""" base class for all the tests"""
import unittest
from flask import json

from ... import create_app
from ...database_config import destroy_tables


class BaseTestCase(unittest.TestCase):

    """ set up configurations for the test environment """
    
    def setUp(self):
        """ set up app configuration """
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.sign_up_user = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronovalerie@gmail.com",
            "phoneNumber": '0717245777',
            "username": "hella",
            "password": "badgirl"
        }
        self.sign_up_user_no_data = {}
        self.sign_up_user_missing_field = {
            "firstname": "Valerie",
            "othernames": "other",
            "email": "ronovaleri@gmail.com",
            "phoneNumber": "0717245777",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_user_empty_string = {
            "firstname": "",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronovaler@gmail.com",
            "phoneNumber": "0717245777",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_user_bad_email = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronovalegmail.com",
            "phoneNumber": "0717245777",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_user_whitespace = {
            "firstname": "uugg",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronoval@gmail.com",
            "phoneNumber": "0717245777",
            "username": " ",
            "password": "abc123"
        }
        self.sign_up_user_special_characters = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "&%&%$",
            "email": "ronova@gmail.com",
            "phoneNumber": "0717245777",
            "username": "&&%%",
            "password": "abc123"
        }
        self.sign_up_user_invalid_phone_number = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronov@gmail.com",
            "phoneNumber": "number",
            "username": "loki",
            "password": "abc123"
        }
        self.log_in_user = {
            "username": "hella",
            "password": "badgirl"
        }
        self.log_in_user_missing_field = {
            "password": "badgirl"
        }
        self.log_in_user_empty_String = {
            "username": "",
            "password": "badgirl"
        }
        self.log_in_user_whitespace = {
            "username": "hella",
            "password": "badgirl"
        }
        self.log_in_user_special_characters = {
            "username": "hella",
            "password": "badgirl"
        }
        self.log_in_wrong_details = {
            "username": "hella",
            "password": "badgir"
        }
        self.post_incident = {
            "type_of_incident": "Redflag",
            "location": "1,7",
            "images": ["blah"],
            "videos": ["blah"],
            "comment": "wow i love this"
        }

        self.post_incident_no_data = {

        }
        self.post_incident_empty_string = {
            "type_of_incident": "Redflag",
            "location": "1,0.9",
            "images": ["blah"],
            "videos": ["blah"],
            "comment": ""
        }
        self.post_incident_whitespace = {
            "type_of_incident": "Redflag",
            "location": "4,8",
            "images": ["blah"],
            "videos": ["blah"],
            "comment": "    "
        }
        self.post_incident_no_field = {
            "type_of_incident": "Redflag",
            "images": ["blah"],
            "videos": ["blah"],
            "comment": "wow ikk juttd"
        }
        self.post_incident_special_characters = {
            "type_of_incident": "Redflag",
            "location": "5,9",
            "images": ["blah"],
            "videos": ["blah"],
            "comment": "&%$^%"
        }
        self.post_incident_not_json = ()
        self.post_incident_not_String = {
            "type_of_incident": "Redflag",
            "location": "9,8.0",
            "images": ["blah"],
            "videos": ["blah"],
            "comment": "wow ugy drrdf"
        }
        self.post_incident_bad_location_format = {
            "type_of_incident": "Redflag",
            "location": "rongai",
            "images": ["blah"],
            "videos": ["blah"],
            "comment": "i am a comment"
        }
        self.edit_incident = {
            "othernames": "others"
        }
        self.edit_incident_status = {
            "status": "pending"
        }
        self.edit_incident_invalid = {
            "type_of_incident": "",
            "location": "",
            "images": "",
            "videos": "",
            "comment": ""
        }
        
        self.edit_incident_location = {
            "location": "rongai"
        }
    
    def register_user(self):

        response = self.client.post('api/v2/users',
                                    data=json.dumps(self.sign_up_user),
                                    headers={'content-type': 'application/json'}
                                    )
        return response

    def login_user(self):

        response = self.client.post(
            'api/v2/users/login', data=json.dumps(self.log_in_user),
            headers={'content-type': 'application/json'}
            )
        return response

    def get_access_token(self):
        self.register_user()
        response = self.login_user()
        self.data = json.loads(response.data)  
        self.token = self.data['access_token']
        print(self.token)

    def create_incident(self, data):
        
        """ post an incident """

        self.get_access_token()
        access_token = self.token
        # import pdb; pdb.set_trace()
        incident = self.client.post(
                                'api/v2/incidents',
                                data=json.dumps(data),
                                headers={
                                    'content-type': 'application/json',
                                    'Authorization': f"Bearer {access_token}"
                                    }
                                )
        return incident

    def edit_any_incident_field(self, data):

        """ edit an incident """

        self.get_access_token()
        access_token = self.token
        incident = self.client.put(
                                'api/v2/incidents/1',
                                data=json.dumps(data),
                                headers={
                                    'content-type': 'application/json',
                                    'Authorization': f"Bearer {access_token}"
                                    }
                                )
        return incident

    def edit_incident_not_found(self, data):

        """ edit an incident """

        self.get_access_token()
        access_token = self.token
        incident = self.client.put(
                                'api/v2/incidents/50',
                                data=json.dumps(data),
                                headers={
                                    'content-type': 'application/json',
                                    'Authorization': f"Bearer {access_token}"
                                    }
                                )
        return incident


    def tearDown(self):
        db_url = self.app.config.get('DATABASE_URL')
        # import pdb; pdb.set_trace()
        
        destroy_tables(url=db_url)

    
if __name__ == '__main__':
    unittest.main()
