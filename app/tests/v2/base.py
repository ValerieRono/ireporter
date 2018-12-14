""" base class for all the tests"""
import unittest

from ... import create_app
from ...database_config import destroy_tables, init_db


class BaseTestCase(unittest.TestCase):

    """ set up configurations for the test environment """

    def setUp(self):
        """ set up app configuration """
        self.app = create_app(config_name="testing")
        self.db = init_db()
        self.client = self.app.test_client()
        self.sign_up_user = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronovalerie@gmail",
            "phoneNumber": "number",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_existing_user = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronovalerie@gmail",
            "phoneNumber": "number",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_user_no_data = {}
        self.sign_up_user_missing_field = {
            "firstname": "Valerie",
            "othernames": "other",
            "email": "ronovalerie@gmail",
            "phoneNumber": "number",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_user_empty_string = {
            "firstname": "",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronovalerie@gmail",
            "phoneNumber": "number",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_user_bad_email = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "other",
            "email": "blah",
            "phoneNumber": "number",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_user_whitespace = {
            "firstname": "    ",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronovalerie@gmail",
            "phoneNumber": "number",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_user_special_characters = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "&%&%$",
            "email": "ronovalerie@gmail",
            "phoneNumber": "number",
            "username": "loki",
            "password": "abc123"
        }
        self.sign_up_user_wrong_phone_number = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronovalerie@gmail",
            "phoneNumber": "number",
            "username": "loki",
            "password": "abc123"
        }
        self.post_incident = {
            "type_of_incident": "Redflag",
            "location": "rongai",
            "images": "blah",
            "videos": "blah",
            "comment": "wow"
        }
        self.post_existing_incident = {
            "type_of_incident": "Redflag",
            "location": "rongai",
            "images": "blah",
            "videos": "blah",
            "comment": "wow"
        }
        self.post_incident_no_data = {

        }
        self.post_incident_empty_string = {
            "type_of_incident": "Redflag",
            "location": "",
            "images": "blah",
            "videos": "blah",
            "comment": "wow"
        }
        self.post_incident_whitespace = {
            "type_of_incident": "Redflag",
            "location": "rongai",
            "images": "     ",
            "videos": "blah",
            "comment": "wow"
        }
        self.post_incident_no_field = {
            "type_of_incident": "Redflag",
            "images": "blah",
            "videos": "blah",
            "comment": "wow"
        }
        self.post_incident_special_characters = {
            "type_of_incident": "Redflag",
            "location": "rongai",
            "images": "blah",
            "videos": "blah",
            "comment": "&%$^%"
        }
        self.post_incident_not_allows = {
            "type_of_incident": "incident",
            "location": "rongai",
            "images": "blah",
            "videos": "blah",
            "comment": "wow"
        }
        self.post_incident_not_String = {
            "type_of_incident": "Redflag",
            "location": "location",
            "images": "blah",
            "videos": "blah",
            "comment": "wow"
        }
        self.post_incident_bad_location_format = {
            "type_of_incident": "Redflag",
            "location": "rongai",
            "images": "blah",
            "videos": "blah",
            "comment": "21332"
        }

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
