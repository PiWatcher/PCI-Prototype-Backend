import json

from tests.TestingSuite import BaseTestingSuite

class TestRolesResource(BaseTestingSuite):
    def setUp(self):
        print("Testing Roles Resources...")
        super().setUp()

        self.user_payload = json.dumps({
            "email": "iotadmin@nau.edu",
            "password": "password"
        })

    def test_successfull_collect_roles(self):
        user_token = self.app.post('/api/auth/signin',
                                 headers={
                                     'Content-Type': 'application/json' 
                                 },
                                 data=self.user_payload).json["jwt_token"]
        
        response = self.app.get('/api/auth/roles',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                })

        self.assertEqual({
            'can_view_raw': True,
            'is_admin': True,
            'role_name': 'admin'
            }, response.json['roles'][0])
        self.assertEqual(200, response.status_code)

    def test_bad_permissions_collect_roles(self):
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

        response = self.app.get('/api/auth/roles',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                })
        
        self.assertEqual('Invalid token.', response.json['message'])
        self.assertEqual(403, response.status_code)
    
    def test_successful_create_role(self):
        user_token = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=json.dumps({
                                        "email": "iotadmin@nau.edu",
                                        "password": "password"
                                    })).json['jwt_token']
        
        response = self.app.post('/api/auth/roles',
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {user_token}'
                                 },
                                 data=json.dumps({
                                     'role_name': 'test_role'
                                 }))
        
        self.assertEqual({
            'role_name': 'test_role',
            'is_admin': False,
            'can_view_raw': False
        }, response.json['new_role'])
        self.assertEqual(200, response.status_code)

    def test_bad_permissions_create_role(self):
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

        response = self.app.get('/api/auth/roles',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {user_token}'
                                },
                                data=json.dumps({
                                    'role_name': 'test_role'
                                }))
        
        self.assertEqual('Invalid token.', response.json['message'])
        self.assertEqual(403, response.status_code)

    def test_successful_delete_role(self):
        admin_token = self.app.post('/api/auth/signin',
                                    headers={
                                        'Content-Type': 'application/json'
                                    },
                                    data=self.user_payload).json['jwt_token']

        response = self.app.delete('/api/auth/roles',
                                   headers={
                                       'Content-Type': 'application/json',
                                       'Authorization': f'Bearer {admin_token}'
                                   },
                                   data=json.dumps({
                                       'role_name': 'public'
                                   }))
        
        self.assertEqual('Successfully deleted public from roles.', response.json['message'])
        self.assertEqual(200, response.status_code)

    def test_bad_permissions_delete_role(self):
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

        response = self.app.delete('/api/auth/roles',
                                    headers={
                                        'Content-Type': 'application/json',
                                        'Authorization': f'Bearer {user_token}'
                                    },
                                    data=json.dumps({
                                        'role_name': 'public'
                                    }))
        
        self.assertEqual('Invalid token.', response.json['message'])
        self.assertEqual(403, response.status_code)
    
    def test_schema_error_delete_role(self):
        user_token = self.app.post('/api/auth/signin',
                                   headers={
                                       'Content-Type': 'application/json'
                                   },
                                   data=self.user_payload).json['jwt_token']

        response = self.app.delete('/api/auth/roles',
                                   headers={
                                       'Content-Type': 'application/json',
                                       'Authorization': f'Bearer {user_token}'
                                   },
                                   data=json.dumps({
                                       'not_a_valid_key': 'randomdata'
                                   }))
        
        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)
    
    def test_role_dne_error_delete_role(self):
        user_token = self.app.post('/api/auth/signin',
                                   headers={
                                       'Content-Type': 'application/json'
                                   },
                                   data=self.user_payload).json['jwt_token']
        
        response = self.app.delete('/api/auth/roles',
                                   headers={
                                       'Content-Type': 'application/json',
                                       'Authorization': f'Bearer {user_token}'
                                   },
                                   data=json.dumps({
                                       'role_name': 'a_role_that_does_not_exist'
                                   }))

        self.assertEqual('That role does not exist.', response.json['message'])
        self.assertEqual(400, response.status_code)

