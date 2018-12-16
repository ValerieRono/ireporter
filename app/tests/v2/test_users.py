"""Test for methods applied to incident records"""
import json

# local import
from app.tests.v2.base import BaseTestCase


class TestRequests(BaseTestCase):

    """Tests"""
    
    def test_new_user(self):
        """Test for registering a new user"""

        # correct request
        response = self.register_user()
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'registered user')

    def test_duplicate_user(self):
        """Test for registering a duplicate user"""
        # duplicate user
        response = self.register_user()
        response2 = self.register_user()
        self.assertEqual(response2.status_code, 400)
        result = json.loads(response2.data)
        self.assertEqual(result["message"], 'username taken!')

    def test_no_input(self):
        # post no data
        response = self.client.post('api/v2/users',
                                    data=json.dumps(self.sign_up_user_no_data),
                                    headers={'content-type': 'application/json'}
                                    )
        self.assertEqual(response.status_code, 400)

    def test_missing_field(self):
        # post invalid data
        response = self.client.post('api/v2/users',
                                    data=json.dumps(self.sign_up_user_missing_field),
                                    headers={'content-type': 'application/json'}
                                    )
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_empty_string(self):

        """Test for signing up a user with empty string for field values"""

        # empty string
        response = self.client.post('api/v2/users',
                                    data=json.dumps(self.sign_up_user_empty_string),
                                    headers={'content-type': 'application/json'}
                                    )
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_wrong_email_format(self):
        """Test for posting a redflag without a comment"""
        # wrong email
        response = self.client.post('api/v2/users',
                                    data=json.dumps(self.sign_up_user_bad_email),
                                    headers={'content-type': 'application/json'}
                                    )
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_whitespaces(self):
        """Test for registering a new user with invalid input data"""
        # whitespaces
        response = self.client.post('api/v2/users',
                                    data=json.dumps(self.sign_up_user_whitespace),
                                    headers={'content-type': 'application/json'}
                                    )
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_special_characters(self):
        """Test for registering a user, with invalid input data"""
        # special characters
        response = self.client.post('api/v2/users',
                                    data=json.dumps(self.sign_up_user_special_characters),
                                    headers={'content-type': 'application/json'}
                                    )
        self.assertEqual(response.status_code, 400)

    def test_new_user_invalid_phone_number(self):

        """Test for registering a user, with invalid input data"""
        
        # invalid phone number
        response = self.client.post('api/v2/users',
                                    data=json.dumps(self.sign_up_user_invalid_phone_number),
                                    headers={'content-type': 'application/json'}
                                    )
        self.assertEqual(response.status_code, 400)

    def test_user_log_in(self):

        """Test for logging in a user, with valid input data"""

        # correct log in
        self.register_user()
        response = self.login_user()
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['message'], "You logged in successfully.")

    def test_login_non_existent(self):

        """ Test for login with correct user details """
        response = self.login_user()
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'], "user not found, please register")

    def test_login_missing_field(self):

        """ Test for login without a username """
        self.register_user()
        response = self.client.post(
            'api/v2/users/login', data=json.dumps(self.log_in_user_missing_field),
            headers={'content-type': 'application/json'}
            )
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message']['username'], "username required")

    def test_login_empty_string(self):

        """ Test for login without a username """
        self.register_user()
        response = self.client.post(
            'api/v2/users/login', data=json.dumps(self.log_in_user_empty_String),
            headers={'content-type': 'application/json'}
            )
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'], "please provide username")

    def test_login_invalid_password(self):
        self.register_user()
        response = self.client.post(
            'api/v2/users/login', data=json.dumps(self.log_in_wrong_details),
            headers={'content-type': 'application/json'}
            )
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Invalid password, Please try again')