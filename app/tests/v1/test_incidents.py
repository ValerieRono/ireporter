"""Test for methods applied to incident records"""
import json

# local import
from app.tests.v1.base import BaseTestCase

class TestRequests(BaseTestCase):

    """Tests"""

    def test_new_incident(self):
        """Test for posting an incident"""
        # correct request
        response = self.client.post('api/v1/incidents', data=json.dumps(
            self.incident), headers={'content-type': "application/json"})
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'created record')

    def test_new_incident_without_comment(self):
        """Test for posting a redflag without a comment"""
        # no body
        response = self.client.post('api/v1/incidents', data=json.dumps(
            self.incident_without_comment),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 400)

    def test_get_all_incidents(self):
        """Test for viewing all redflags"""
        # get all
        response = self.client.get('api/v1/incidents')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'successfull')

    def test_get_specific_incident(self):
        """Test for viewing a particular redflag"""
        # existing redflag
        response = self.client.post('api/v1/incidents', data=json.dumps(
            self.incident), headers={'content-type': "application/json"})
        self.assertEqual(response.status_code, 201)
        response = self.client.get(
            'api/v1/incidents/1', headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'successfull')

    def test_get_incident_not_found(self):
        """Test for viewing a redflag that does not exist"""
        # redflag does not exist
        response = self.client.get('api/v1/incidents/20')
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'record not found')

    def test_edit_incident_not_found(self):
        """Test for editing a redflag that does not exist"""
        # redflag does not exist
        response = self.client.put('api/v1/incidents/20')
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'record not found')

    def test_delete_incident_not_found(self):
        """Test for viewing a redflag that does not exist"""
        # redflag does not exist
        response = self.client.delete('api/v1/incidents/20')
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'record not found')

    def test_edit_an_incident(self): 
        """Test for modifying a redflag """
        # edit existing record
        response = self.client.post('api/v1/incidents', data=json.dumps(
            self.incident), headers={'content-type': "application/json"})
        self.assertEqual(response.status_code, 201)
        response = self.client.put(
            'api/v1/incidents/1',
            data=json.dumps(self.update_incident),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'updated record')

    def test_user_delete_incident(self):
        """Test for deleting a redflag"""
        # delete existing record
        response = self.client.delete('api/v1/incidents/2')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'deleted')

    def test_no_input(self):
        # post no data
        response = self.client.post(
            'api/v1/incidents',
            data=json.dumps(self.no_input),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 400)