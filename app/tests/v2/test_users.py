"""Test for methods applied to incident records"""
import json

# local import
from app.tests.v2.base import BaseTestCase


class TestRequests(BaseTestCase):

    """Tests"""

    def test_new_user(self):
        """Test for registering a new user"""
        # correct request
        response = self.client.post('api/v2/users', data=json.dumps(
            self.sign_up_user), headers={'content-type': "application/json"})
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'registered user')

    def test_duplicate_user(self):
        """Test for registering a duplicate user"""
        # duplicate user
        response = self.client.post(
            'api/v2/users', data=json.dumps(self.sign_up_existing_user),
            headers={'content-type': "application/json"})
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'user exists!')

    def test_no_input(self):
        # post no data
        response = self.client.post(
            'api/v2/users',
            data=json.dumps(self.sign_up_user_no_data),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 400)

    def test_missing_field(self):
        # post invalid data
        response = self.client.post(
            'api/v2/users',
            data=json.dumps(self.sign_up_user_missing_field),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_empty_string(self):
        """Test for signing up a user with empty stringd for field values"""
        # empty string
        response = self.client.post('api/v2/users', data=json.dumps(
            self.sign_up_user_empty_string),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_wrong_email_format(self):
        """Test for posting a redflag without a comment"""
        # wrong email
        response = self.client.post('api/v2/users', data=json.dumps(
            self.sign_up_user_bad_email),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_whitespaces(self):
        """Test for registering a new user with invalid input data"""
        # whitespaces
        response = self.client.post('api/v2/users', data=json.dumps(
            self.sign_up_user_whitespace),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_special_characters(self):
        """Test for registering a user, with invalid input data"""
        # special characters
        response = self.client.post('api/v2/users', data=json.dumps(
            self.sign_up_user_special_characters),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 400)

    def test_new_user_wrong_phone_number(self):
        """Test for registering a user, with invalid input data"""
        # special characters
        response = self.client.post('api/v2/users', data=json.dumps(
            self.sign_up_user_wrong_phone_number),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 400)

    # def test_get_all_incidents(self):
    #     """Test for viewing all redflags"""
    #     # get all
    #     response = self.client.get('api/v1/incidents')
    #     self.assertEqual(response.status_code, 200)
    #     result = json.loads(response.data)
    #     self.assertEqual(result['data'][0]["message"], 'successfull')

    # def test_get_specific_incident(self):
    #     """Test for viewing a particular redflag"""
    #     # existing redflag
    #     response = self.client.post('api/v1/incidents', data=json.dumps(
    #         self.incident), headers={'content-type': "application/json"})
    #     self.assertEqual(response.status_code, 201)
    #     response = self.client.get(
    #         'api/v1/incidents/1', headers={'content-type': 'application/json'}
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     result = json.loads(response.data)
    #     self.assertEqual(result['data'][0]["message"], 'successfull')

    # def test_get_incident_not_found(self):
    #     """Test for viewing a redflag that does not exist"""
    #     # redflag does not exist
    #     response = self.client.get('api/v1/incidents/20')
    #     self.assertEqual(response.status_code, 404)
    #     result = json.loads(response.data)
    #     self.assertEqual(result['data'][0]["message"], 'record not found')

    # def test_edit_incident_not_found(self):
    #     """Test for editing a redflag that does not exist"""
    #     # redflag does not exist
    #     response = self.client.put('api/v1/incidents/20')
    #     self.assertEqual(response.status_code, 404)
    #     result = json.loads(response.data)
    #     self.assertEqual(result['data'][0]["message"], 'record not found')

    # def test_delete_incident_not_found(self):
    #     """Test for viewing a redflag that does not exist"""
    #     # redflag does not exist
    #     response = self.client.delete('api/v1/incidents/20')
    #     self.assertEqual(response.status_code, 404)
    #     result = json.loads(response.data)
    #     self.assertEqual(result['data'][0]["message"], 'record not found')

    # def test_edit_an_incident(self): 
    #     """Test for modifying a redflag """
    #     # edit existing record
    #     response = self.client.post('api/v1/incidents', data=json.dumps(
    #         self.incident), headers={'content-type': "application/json"})
    #     self.assertEqual(response.status_code, 201)
    #     response = self.client.put(
    #         'api/v1/incidents/1',
    #         data=json.dumps(self.update_incident),
    #         headers={'content-type': "application/json"}
    #         )
    #     self.assertEqual(response.status_code, 200)
    #     result = json.loads(response.data)
    #     self.assertEqual(result['data'][0]["message"], 'updated record')

    # def test_user_delete_incident(self):
    #     """Test for deleting a redflag"""
    #     # delete existing record
    #     response = self.client.delete('api/v1/incidents/2')
    #     self.assertEqual(response.status_code, 200)
    #     result = json.loads(response.data)
    #     self.assertEqual(result['data'][0]["message"], 'deleted')

    # def test_no_input(self):
    #     # post no data
    #     response = self.client.post(
    #         'api/v1/incidents',
    #         data=json.dumps(self.no_input),
    #         headers={'content-type': "application/json"}
    #         )
    #     self.assertEqual(response.status_code, 400)