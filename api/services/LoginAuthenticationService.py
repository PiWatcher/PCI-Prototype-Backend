import api
import json
import bcrypt

from flask import Response
from bson import json_util

class LoginAuthenticationService():

    def __init__(self):
        self.mongo = api.mongo
        self.database = self.mongo['Users']
        self.collection = self.database['users']

    def __hash_password(self, password):
        # hashes password and returns new password
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def handle_signin(self, data):
        return self.__signin(data)

    def handle_signup(self, data):
        return self.__signup(data) 

    def __signin(self, data):
        pass

    def __signup(self, data):
        # check if user exists
        if not self.__user_exists(data['email']):
            # build new json
            user = {
                'email': data['email'],
                'password': self.__hash_password(data['password'].encode('utf-8')),
                'name': data['name'],
                'user_type': data['user_type']
            }

            # insert new user
            self.collection.insert_one(user)

            json_response = {
                'status': 201,
                'description': f'New {data["user_type"]} account was created!'
            }

            return Response(json.dumps(json_response, default=json_util.default),
                            mimetype='application/json',
                            status=json_response['status'])
        
        json_response = {
            'status': 409,
            'description': 'User with that email already exists!'
        }

        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])

    def __user_exists(self, email):
        # find user in the database by email
        potential_user = self.collection.find_one({'email': email})

        # if user exists
        if potential_user:
            return True
        
        return False
