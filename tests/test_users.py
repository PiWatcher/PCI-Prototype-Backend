import json

from tests.TestingSuite import BaseTestingSuite

class TestUsersResource(BaseTestingSuite):
    def setUp(self):
        print('Testing Users resources...')
        super().setUp()

        self.user_payload = json.dumps({
            "email": "iotadmin@nau.edu",
            "password": "password"
        })
    
    def test_successful_grab_users(self):
        user_token = self.app.post('/api/auth/signin',
                                  headers={
                                      'Content-Type': 'application/json'
                                  },
                                  data=self.user_payload).json['jwt_token']
        
        response = self.app.get('/api/auth/users',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                })

        self.assertEqual({
            "email": "iotadmin@nau.edu",
            "full_name": "Administrator",
            "role": "admin"
        }, response.json['users'][0])
        self.assertEqual(200, response.status_code)

    def test_bad_permissions_grab_users(self):
        test_user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": 'testpassword',
            'full_name': 'test_user'
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)

        user_token  = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=json.dumps({
                                        "email": "testuser@test.com",
                                        "password": "testpassword",
                                    })).json['jwt_token']

        response = self.app.get('/api/auth/users',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                })
        
        self.assertEqual('Invalid token.', response.json['message'])
        self.assertEqual(403, response.status_code)

    def test_successful_delete_user(self):
        test_user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": "testpassword",
            "full_name": "test_user"
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)
        
        user_token = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=self.user_payload).json['jwt_token']
        
        response = self.app.delete('/api/auth/users',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                },
                                data=json.dumps({
                                    'email': 'testuser@test.com'
                                }))

        self.assertEqual('Successfully deleted testuser@test.com from database', response.json['message'])
        self.assertEqual(200, response.status_code)

    def test_bad_permissions_delete_user(self):
        test_user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": "testpassword",
            "full_name": "test_user"
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json',
                      },
                      data=test_user_payload)

        user_token = self.app.post('/api/auth/signin',
                                   headers={
                                       'Content-Type': 'application/json'
                                   },
                                   data=test_user_payload).json['jwt_token']

        response= self.app.delete('/api/auth/users',
                                   headers={
                                       'Content-Type': 'application/json',
                                       'Authorization': f'Bearer {user_token}'
                                   },
                                   data=json.dumps({
                                       'email': 'testuser@test.com'
                                   }))
        
        self.assertEqual('Invalid token.', response.json['message'])
        self.assertEqual(403, response.status_code)

    def test_bad_schema_error_delete_user(self):
        test_user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": "testpassword",
            "full_name": "test_user"
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)
        
        user_token = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=self.user_payload).json['jwt_token']
        
        response = self.app.delete('/api/auth/users',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                },
                                data=json.dumps({
                                    'bad_key': 'testuser@test.com'
                                }))

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_email_dne_error_delete_user(self):
        user_token = self.app.post('/api/auth/signin',
                        headers={
                            'Content-Type': 'application/json'
                        },
                        data=self.user_payload).json['jwt_token']

        response = self.app.delete('/api/auth/users',
                                   headers={
                                       'Content-Type': 'application/json',
                                       'Authorization': f'Bearer {user_token}'
                                   },
                                   data=json.dumps({
                                       "email": "user_dne@dne.com"
                                   }))
        
        self.assertEqual("Couldn't find the user with given email address.", response.json['message'])
        self.assertEqual(400, response.status_code)
        
    def test_successful_user_role_update(self):
        test_user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": "testpassword",
            "full_name": "test_user"
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)
        
        user_token = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=self.user_payload).json['jwt_token']

        response = self.app.post('/api/auth/users/update',
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {user_token}'
                                 },
                                 data=json.dumps({
                                     "email": "testuser@test.com",
                                     "new_role": "admin"
                                 }))
        
        self.assertEqual({
            'email': 'testuser@test.com',
            'full_name': 'test_user',
            'role': 'admin'
        }, response.json['user'])
        self.assertEqual(200, response.status_code)

    def test_bad_permissions_user_role_update(self):
        test_user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": "testpassword",
            "full_name": "test_user"
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)
        
        user_token = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=test_user_payload).json['jwt_token']
        
        response = self.app.post('/api/auth/users/update',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                },
                                data=json.dumps({
                                    "email": "testuser@test.com",
                                    "new_role": "admin"
                                }))

        self.assertEqual('Invalid token.', response.json['message'])
        self.assertEqual(403, response.status_code)

    def test_email_dne_error_update_user_role(self):
        user_token = self.app.post('/api/auth/signin',
                                   headers={
                                       'Content-Type': 'application/json'
                                   },
                                   data=self.user_payload).json['jwt_token']
        
        response = self.app.post('/api/auth/users/update',
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {user_token}'
                                 },
                                 data=json.dumps({
                                     "email": "testuser@test.com",
                                     "new_role": "admin"
                                 }))

        self.assertEqual("Couldn't find the user with given email address.", response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_bad_schema_error_update_user_role(self):
        test_user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": "testpassword",
            "full_name": "test_user"
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)
        
        user_token = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=self.user_payload).json['jwt_token']
        
        response = self.app.post('/api/auth/users/update',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                },
                                data=json.dumps({
                                    'bad_key': 'testuser@test.com',
                                    'new_role': 'admin'
                                }))

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)
    
    def test_role_dne_error_update_user_role(self):
        test_user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": "testpassword",
            "full_name": "test_user"
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)
        
        user_token = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=self.user_payload).json['jwt_token']
        
        response = self.app.post('/api/auth/users/update',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                },
                                data=json.dumps({
                                    'email': 'testuser@test.com',
                                    'new_role': 'rolethatdoesnotexist'
                                }))

        self.assertEqual('That role does not exist.', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_successful_user_password_update(self):
        test_user_payload = json.dumps({
            "email": "testuser@test.com",
            "password": "testpassword",
            "full_name": "test_user"
        })

        self.app.post("/api/auth/signup",
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)
        
        user_token = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=test_user_payload).json['jwt_token']

        response = self.app.post('/api/auth/users/update/password',
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {user_token}'
                                 },
                                 data=json.dumps({
                                    'password': 'testpassword',
                                    'new_password': 'newpassword'
                                 }))

        self.assertEqual('testuser@test.com password was updated', response.json['description'])
        self.assertEqual(200, response.status_code)

    def test_bad_schema_error_user_password_update(self):
        test_user_payload = json.dumps({
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'full_name': 'test_user'
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)

        user_token = self.app.post('/api/auth/signin',
                                   headers={
                                       'Content-Type': 'application/json'
                                   },
                                   data=test_user_payload).json['jwt_token']
        
        response = self.app.post('/api/auth/users/update/password',
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {user_token}'
                                 },
                                 data=json.dumps({
                                     'password': 'testpassword',
                                     'bad_key': 'badbadbad'
                                 }))

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_unauthorized_password_user_password_update(self):
        test_user_payload = json.dumps({
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'full_name': 'test_user'
        })

        self.app.post('/api/auth/signup',
                      headers={
                          'Content-Type': 'application/json'
                      },
                      data=test_user_payload)

        user_token = self.app.post('/api/auth/signin',
                                   headers={
                                       'Content-Type': 'application/json'
                                   },
                                   data=test_user_payload).json['jwt_token']
        
        response = self.app.post('/api/auth/users/update/password',
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {user_token}'
                                 },
                                 data=json.dumps({
                                     'password': 'wrongpassword',
                                     'new_password': 'newpassword'
                                 }))