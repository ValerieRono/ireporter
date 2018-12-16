"""Test for methods applied to incident records"""
import json

# local import
from app.tests.v2.base import BaseTestCase


class TestRequests(BaseTestCase):

    """Tests"""

    def test_create_new_incident(self):

        """Test for creating a new incident"""

        # authorised
        response = self.create_incident(self.post_incident)
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "created incident record")

    # def test_create_duplicate_incident(self):

    #     """ Test for creating an incident that already exists """

    #     self.create_incident(self.post_incident)
    #     response = self.create_incident(self.post_incident)
    #     self.assertEqual(response.status_code, 400)
    #     result = json.loads(response.data)
    #     self.assertEqual(result['data'][0]['message'], "incident exists")
    
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
        self.assertEqual(result['message'], 'Authorization required!')

    def test_new_incident_no_comment(self):

        """Test for posting an incident without comment"""
        
        # no comment
        response = self.create_incident(self.post_incident_empty_string)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        # import pdb; pdb.set_trace()
        self.assertEqual(result['message']['comment'], "please comment")

    def test_no_input(self):

        """Test for posting an incident without data"""

        # post no data
        response = self.create_incident(self.post_incident_no_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        expected = "type can only be Redflag or Intervention"
        self.assertEqual(result['message']['type_of_incident'], expected)

    def test_missing_field(self):

        """Test for posting an incident with missing data"""

        # post missing field
        response = self.create_incident(self.post_incident_no_field)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        # import pdb; pdb.set_trace()
        self.assertEqual(result['message']['location'], "wrong location format")

    def test_new_incident_with_wrong_location_format(self):

        """Test for posting an incident with wrong location format"""

        # post wrong location format
        response = self.create_incident(self.post_incident_bad_location_format)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        # import pdb; pdb.set_trace()
        self.assertEqual(result['message']['location'], "wrong location format")

    def test_new_incident_with_whitespaces(self):

        """Test for posting an incident with whitespaces"""

        # post white spaces
        response = self.create_incident(self.post_incident_whitespace)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        # import pdb; pdb.set_trace()
        self.assertEqual(result['message']['comment'], "please comment")

    def test_new_incident_with_special_characters(self):

        """Test for posting an incident with special characters"""

        # post special characters
        response = self.create_incident(self.post_incident_not_json)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        # import pdb; pdb.set_trace()
        self.assertEqual(result['message']['type_of_incident'], "type can only be Redflag or Intervention")

    def test_post_incident_not_json(self):

        """Test for posting an incident with no-json input"""

        # not json
        response = self.create_incident(self.post_incident_special_characters)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        # import pdb; pdb.set_trace()
        self.assertEqual(result['message']['comment'], "please comment")

    def test_view_all_incidents(self):

        """Test for viewing all incidents"""

        self.create_incident(self.post_incident)
        access_token = self.token
        response = self.client.get(
            'api/v2/incidents',
            headers={
                'content-type': 'application/json',
                'Authorization': f"Bearer {access_token}"
            }
        )
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "successfull")

    def test_view_an_incident(self):

        """Test for viewing a specific incident"""
        
        self.create_incident(self.post_incident)
        access_token = self.token
        response = self.client.get(
            'api/v2/incidents/1',
            headers={
                'content-type': 'application/json',
                'Authorization': f"Bearer {access_token}"
            }
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "successfull")

    def test_view_incident_not_found(self):

        """Test for viewing an incident that does not exist"""
        # incident does not exist
        self.create_incident(self.post_incident)
        access_token = self.token
        response = self.client.get(
            'api/v2/incidents/56',
            headers={
                'content-type': 'application/json',
                'Authorization': f"Bearer {access_token}"
            }
        )
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'], "incident not found")

    def test_edit_any_field(self):

        """Test for modifying any incident field """

        self.create_incident(self.post_incident)
        response = self.edit_any_incident_field(self.edit_incident)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "successfully edited record")

    def test_edit_location_bad_input(self):

        """Test for modifying an incident location """

        self.create_incident(self.post_incident)
        response = self.edit_any_incident_field(self.edit_incident_location)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        # import pdb; pdb.set_trace()
        self.assertEqual(
                        result['message']['location'],
                        '''Value does not match pattern: "^(\\-?\\d+(\\.\\d+)?),\\s*(\\-?\\d+(\\.\\d+)?)$"'''
                        )

    def test_delete_an_incident(self):

        """Test for deleting a redflag"""
        self.create_incident(self.post_incident)
        access_token = self.token
        
        response = self.client.delete(
                                'api/v2/incidents/1',
                                headers={'Authorization': "Bearer " + access_token}
                                )
        # import pdb; pdb.set_trace()
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
        self.assertEqual(result['message'], "Record not found")

    def test_edit_incident_invalid_data(self):

        """Test for updating an incident using invalid data"""
        self.create_incident(self.post_incident)
        response = self.edit_any_incident_field(self.edit_incident_invalid)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        expected = 'type can only be Redflag or Intervention'
        self.assertEqual(result['message']['type_of_incident'], expected)

    def test_edit_incident_not_found(self):

        """Test for updating an incident"""
        self.create_incident(self.post_incident)
        response = self.edit_incident_not_found(self.edit_incident)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'], "Record not found")
