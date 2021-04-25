import json

from tests.TestingSuite import BaseTestingSuite

class TestSignupResource(BaseTestingSuite):
    def setUp(self):
        print("Testing Signup Resources...")
        super().setUp()

    def test_successful_signup(self):
        # create payload
        payload = json.dumps({
            "email": 'testemail@test.com',
            "password": 'testpassword',
            "full_name": 'test name'
        })

        # create response
        response = self.app.post('/api/auth/signup',
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 data=payload)

        self.assertEqual('New public account was created!', response.json['message'])
        self.assertEqual(201, response.status_code)
    
    def test_unsuccessful_signup(self):
        # create payload
        payload = json.dumps({
            "email": "testemail@test.com",
            "password": "testpassword",
            # missing full_name
        })

        # create response
        response = self.app.post('/api/auth/signup',
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 data=payload)
        
        self.assertEqual("Request is missing required fields.", response.json["message"])
        self.assertEqual(400, response.status_code)
    
    def test_email_already_exists(self):
        # create payload
        payload = json.dumps({
            "email": 'testemail@test.com',
            "password": "testpassword",
            "full_name": "test user"
        })

        response = self.app.post('/api/auth/signup',
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 data=payload)

        # create another payload
        payload = json.dumps({
            "email": 'testemail@test.com', # same email
            "password": "adifferentpassword",
            "full_name": "test user"
        })

        response = self.app.post('/api/auth/signup',
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 data=payload)
        
        self.assertEqual("An account with that given email address already exists.", response.json["message"])
        self.assertEqual(400, response.status_code)
