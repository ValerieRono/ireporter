""" base class for all the tests"""
import unittest

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
            "email": "ronovalerie@gmail",
            "phoneNumber": "number",
            "username": "hella",
            "password": "badgirl"
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
        self.sign_up_user_invalid_phone_number = {
            "firstname": "Valerie",
            "lastname": "Rono",
            "othernames": "other",
            "email": "ronovalerie@gmail",
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
            "username": "hella",
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
            "location": "rongai",
            "images": "blah",
            "videos": "blah",
            "comment": "wow"
        }

        self.post_incident_no_data = {

        }
        self.post_incident_empty_string = {
            "type_of_incident": "Redflag",
            "location": "blah",
            "images": "blah",
            "videos": "blah",
            "comment": ""
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
        self.post_incident_not_json = ()
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
        self.edit_incident = {
            "othernames": "others"
        }
        self.edit_incident_status = {
            "status": "Resolved"
        }
        self.edit_incident_invalid = {
            "othernames": ""
        }
        self.edit_incident_no_input = ()
        self.edit_incident_location = {
            "location": "location"
        }

    def tearDown(self):
        db_url = self.app.config.get('DATABASE_URL')
        # import pdb; pdb.set_trace()
        destroy_tables(url=db_url)


if __name__ == '__main__':
    unittest.main()
