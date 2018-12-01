""" base class for all the tests"""
import unittest
import datetime as dt

from ... import create_app

class BaseTestCase(unittest.TestCase):
    """ set up configurations for the test environment"""
    @classmethod
    def setUpClass(self):
        """set up app configuration"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.data = [{

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
    }]
        

        self.incident = { 
            "createdBy" : "Valerie Rono", 
            "type_of_incident" : "RedFlag",
            "location" : "coordinates",
            "status": "pending",
            "images" : "file path", 
            "videos" : "file path",
            "comment" : "traffic police bribery"
            }

        self.update_incident = { 
            "createdBy" : "Valerie Rono", 
            "type_of_incident" : "RedFlag",
            "location" : "coordinates",
            "status": "pending",
            "images" : "file path", 
            "videos" : "file path",
            "comment" : "power outage"
        }
        self.incident_without_comment = {
            "createdBy" : "Valerie Rono", 
            "type_of_incident" : "RedFlag",
            "location" : "coordinates",
            "status": "pending",
            "images" : "file path", 
            "videos" : "file path",
            "comment" : ""
        }
        self.no_input = {
            
        }

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()