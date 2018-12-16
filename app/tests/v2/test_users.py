"""Test for methods applied to incident records"""
import json

# local import
from app.tests.v2.base import BaseTestCase


class TestRequests(BaseTestCase):

    """Tests"""
    def register_user(self, user):

        """ sign up test user """

        response = self.client.post('api/v2/users',
                                    data=json.dumps(user),
                                    headers={'content-type': 'application/json'}
                                    )
        return response

    def login_user(self, user):
         
        """ sign in a user """

        response = self.client.post(
            'api/v2/user', data=json.dumps(user),
            headers={'content-type': 'application/json'}
            )
        return response

    def test_new_user(self):
        """Test for registering a new user"""

        # correct request
        response = self.register_user(self.sign_up_user)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'registered user')

    def test_duplicate_user(self):
        """Test for registering a duplicate user"""
        # duplicate user
        self.register_user(self.sign_up_user)
        response = self.register_user(self.sign_up_user)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]["message"], 'user exists!')

    def test_no_input(self):
        # post no data
        response = self.register_user(self.sign_up_user_no_data)
        self.assertEqual(response.status_code, 400)

    def test_missing_field(self):
        # post invalid data
        response = self.register_user(self.sign_up_user_missing_field)
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_empty_string(self):

        """Test for signing up a user with empty string for field values"""

        # empty string
        response = self.register_user(self.sign_up_user_empty_string)
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_wrong_email_format(self):
        """Test for posting a redflag without a comment"""
        # wrong email
        response = self.register_user(self.sign_up_user_bad_email)
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_whitespaces(self):
        """Test for registering a new user with invalid input data"""
        # whitespaces
        response = self.register_user(self.sign_up_user_whitespace)
        self.assertEqual(response.status_code, 400)

    def test_new_user_with_special_characters(self):
        """Test for registering a user, with invalid input data"""
        # special characters
        response = self.register_user(self.sign_up_user_special_characters)
        self.assertEqual(response.status_code, 400)

    def test_new_user_invalid_phone_number(self):

        """Test for registering a user, with invalid input data"""
        
        # invalid phone number
        response = self.register_user(self.sign_up_user_invalid_phone_number)
        self.assertEqual(response.status_code, 400)

    def test_user_log_in(self):

        """Test for logging in a user, with valid input data"""

        # correct log in
        self.register_user(self.sign_up_user)
        response = self.login_user(self.log_in_user)
        self.assertEqual(response.status_code, 201)
        response = self.client.post('api/v2/user', data=json.dumps(
            self.log_in_user),
            headers={'content-type': "application/json"}
            )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "successful")

    def test_login_non_existent(self):

        """ Test for login with correct user details """

        response = self.login_user(self.log_in_user)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "user not found, sign up first")

    def test_login_missing_field(self):

        """ Test for login without a username """

        response = self.login_user(self.log_in_user_missing_field)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "please provide input")

    def test_login_empty_string(self):

        """ Test for login without a username """

        response = self.login_user(self.log_in_user_empty_String)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "please provide input")

    def test_login_whitespace(self):

        """ Test for login without a username """

        response = self.login_user(self.log_in_user_whitespace)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "please provide input")

    def test_login_special_characters(self):

        """ Test for login without a username """

        response = self.login_user(self.log_in_user_special_characters)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "please provide input")

    def test_login_invalid_password(self):

        """ Test for login without a username """
        self.register_user(self.sign_up_user)
        response = self.login_user(self.log_in_wrong_details)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['data'][0]['message'], "password is wrong, try again")