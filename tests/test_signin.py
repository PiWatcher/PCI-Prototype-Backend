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
    
    def test_successful_token_signin(self):
        response = self.app.post('/api/auth/signin',
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 data=self.user_payload)
        
        response = self.app.post('/api/auth/token',
                                 headers={
                                     "Content-Type": "application/json",
                                     "Authorization": f'Bearer {response.json["jwt_token"]}'
                                 })

        self.assertEqual('test_user', response.json["full_name"])
        self.assertEqual(200, response.status_code)

    def test_unsuccessful_token_signin(self):
        response = self.app.post('/api/auth/token',
                                 headers={
                                     "Content-Type": "application/json",
                                     "Authorization": "Bearer invalidjwt"
                                 })

        self.assertEqual('Not enough segments', response.json['msg'])
    
    def test_missing_jwt_token_signin(self):
        response = self.app.post('/api/auth/token',
                                 headers={
                                     "Content-Type": "application/json"
                                 })
        
        
        self.assertEqual('Missing Authorization Header', response.json["msg"])