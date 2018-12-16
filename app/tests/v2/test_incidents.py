"""Test for methods applied to incident records"""
import json

# local import
from app.tests.v2.base import BaseTestCase


class TestRequests(BaseTestCase):

    """Tests"""
    def register_user(self):

        """ sign up test user """

        response = self.client.post('api/v2/users',
                                    data=json.dumps(self.sign_up_user),
                                    headers={'content-type': 'application/json'}
                                    )
        return response

    def login_user(self):
         
        """ sign in a user """

        response = self.client.post(
            'api/v2/user', data=json.dumps(self.log_in_user),
            headers={'content-type': 'application/json'}
            )
        return response

    def get_access_token(self):
        
        """ get jwt token """

        self.register_user()
        response = self.login_user()
        self.data = json.loads(response.data)   
        self.token = self.data['access_token']

        return self.token

    def create_incident(self, data):
        
        """ post an incident """

        self.get_access_token()
        access_token = self.token
        incident = self.client.post(
                                'api/v2/incidents',
                                data=json.dumps(data),
                                headers={'Authorization': "Bearer " + access_token}
                                )
        return incident

    def edit_any_incident_field(self, data):

        """ edit an incident """

        self.get_access_token()
        access_token = self.token
        incident = self.client.put(
                                'api/v2/incidents/1',
                                data=json.dumps(data),
                                headers={'Authorization': "Bearer " + access_token}
                                )
        return incident

    def edit_incident_not_found(self, data):

        """ edit an incident """

        self.get_access_token()
        access_token = self.token
        incident = self.client.put(
                                'api/v2/incidents/50',
                                data=json.dumps(data),
                                headers={'Authorization': "Bearer " + access_token}
                                )
        return incident

    def test_create_new_incident(self):

        """Test for creating a new incident"""

        # authorised
        response = self.create_incident(self.post_incident)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "created incident record")

    def test_create_duplicate_incident(self):

        """ Test for creating an incident that already exists """

        self.create_incident(self.post_incident)
        response = self.create_incident(self.post_incident)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "incident exists")
    
    def test_create_incident_not_logged_in(self):

        """Test for posting an incident"""

        # correct request, missing token
        response = self.client.post(
                                    'api/v2/incidents',
                                    data=json.dumps(self.post_incident),
                                    headers={'content-type': 'application/json'}
                                    )
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "unauthorized")

    def test_new_incident_no_comment(self):

        """Test for posting an incident without comment"""
        
        # no comment
        response = self.create_incident(self.post_incident_empty_string)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "please comment")

    def test_no_input(self):

        """Test for posting an incident without data"""

        # post no data
        response = self.create_incident(self.post_incident_no_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "please provide input")

    def test_missing_field(self):

        """Test for posting an incident with missing data"""

        # post missing field
        response = self.create_incident(self.post_incident_no_field)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "input data missing")

    def test_new_user_with_wrong_location_format(self):

        """Test for posting an incident with missing data"""

        # post wrong email
        response = self.create_incident(self.post_incident_bad_location_format)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "please provide correct location")

    def test_new_incident_with_whitespaces(self):

        """Test for posting an incident with whitespaces"""

        # post white spaces
        response = self.create_incident(self.post_incident_whitespace)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "invalid input data")

    def test_new_incident_with_special_characters(self):

        """Test for posting an incident with special characters"""

        # post special characters
        response = self.create_incident(self.post_incident_not_json)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "invalid input data")

    def test_post_incident_not_json(self):

        """Test for posting an incident with no-json input"""

        # not json
        response = self.create_incident(self.post_incident_special_characters)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "invalid input data")

    def test_view_all_incidents(self):

        """Test for viewing all incidents"""

        self.create_incident(self.post_incident)
        response = self.client.get('api/v2/incidents')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "successful")

    def test_view_an_incident(self):

        """Test for viewing a specific incident"""
        
        self.create_incident(self.post_incident)
        response = self.client.get('api/v2/incidents/1')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "successful")

    def test_view_incident_not_found(self):

        """Test for viewing an incident that does not exist"""
        # incident does not exist
        self.create_incident(self.post_incident)
        response = self.client.get('api/v2/incidents/56')
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "incident not found")

    def test_edit_any_field(self):

        """Test for modifying any incident field """

        self.create_incident(self.post_incident)
        response = self.edit_any_incident_field(self.edit_incident)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "updated incident")

    def test_edit_bad_input(self):

        """Test for modifying an incident location """

        self.create_incident(self.post_incident)
        response = self.edit_any_incident_field(self.edit_incident_location)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "updated incident")

    def test_delete_an_incident(self):

        """Test for deleting a redflag"""
        self.create_incident(self.post_incident)
        access_token = self.token
        response = self.client.delete(
                                'api/v2/incidents/1',
                                headers={'Authorization': "Bearer " + access_token}
                                )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "successfully deleted record")

    def test_delete_incident_not_found(self):

        self.create_incident(self.post_incident)
        access_token = self.token
        response = self.client.delete(
                                      'api/v2/incidents/50',
                                      headers={'Authorization': "Bearer " + access_token}
                                     )
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "incident not found")

    def test_edit_incident_invalid_data(self):

        """Test for updating an incident using invalid data"""
        self.create_incident(self.post_incident)
        response = self.edit_any_incident_field(self.edit_incident_invalid)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "invalid input")

    def test_edit_incident_not_found(self):

        """Test for updating an incident"""
        self.create_incident(self.post_incident)
        response = self.edit_incident_not_found(self.edit_incident)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "incident not found")

    def test_edit_incident_invalid_input(self):
        """Test for updating an incident"""

        self.create_incident(self.post_incident)        
        response = self.edit_any_incident_field(self.edit_incident_no_input)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "invalid input data")