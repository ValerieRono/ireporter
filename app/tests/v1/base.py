""" base class for all the tests"""
import unittest

from ... import create_app

class BaseTestCase(unittest.TestCase):

    """ set up configurations for the test environment """

    def setUp(self):
        """ set up app configuration """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.data = [{

            "id": 1,
            "createdOn": "some date",
            "createdBy": "Valerie Rono",
            "type_of_incident": "RedFlag",
            "location": "coordinates",
            "status": "resolved",
            "images": "file path",
            "videos": "file path",
            "comment": "traffic police bribery"
        }]

        self.incident = {
            "createdBy": "valerie",
            "type_of_incident": "Redflag",
            "location": "rongai",
            "images": "blah",
            "videos": "blah",
            "comment": "wow"
        }

        self.update_incident = {
            "createdBy": "Someone else",
        }

        self.update_incident_under_pending = {
            "createdBy": "Valerie Rono",
            "type_of_incident": "RedFlag",
            "location": "coordinates",
            "status": "pending",
            "images": "file path",
            "videos": "file path",
            "comment": "power outage"
        }
        self.incident_without_comment = {
            "createdBy": "Valerie Rono",
            "type_of_incident": "RedFlag",
            "location": "coordinates",
            "status": "under investigation",
            "images": "file path",
            "videos": "file path",
            "comment": ""
        }
        self.no_input = {

        }

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
