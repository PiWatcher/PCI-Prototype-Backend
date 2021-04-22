import json

from tests.TestingSuite import BaseTestingSuite

class TestSigninResource(BaseTestingSuite):
    def setUp(self):
        super().setUp()
        self.user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": "testpasssword",
            "full_name": "test_user"
        })

        # create user
        self.app.post('/api/auth/signup',
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 data=self.user_payload)
        

    def test_successful_signin(self):
        # create response
        response = self.app.post('/api/auth/signin',
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 data=self.user_payload)
        
        self.assertEqual('test_user', response.json["full_name"])
        self.assertEqual(str, type(response.json["jwt_token"]))
        self.assertEqual(200, response.status_code)

    def test_unsuccessful_signin(self):

        payload = json.dumps({
            "email": "testuser@test.com",
            "password": "wrongpassword"
        })

        # create response
        response = self.app.post('/api/auth/signin',
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 data=payload)

        self.assertEqual("Invalid username or password.", response.json["message"])
        self.assertEqual(401, response.status_code)
    
    def test_missing_values_in_schema(self):

        payload = json.dumps({
            "email": "testuser@test.com",
        })

        # create response
        response = self.app.post('/api/auth/signin',
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 data=payload)
        
        self.assertEqual("Request is missing required fields.", response.json["message"])
        self.assertEqual(400, response.status_code)