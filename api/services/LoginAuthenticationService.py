import api
import json
import bcrypt

from flask import Response
from flask_httpauth import HTTPBasicAuth
from bson import json_util

class LoginAuthenticationService():

    def __init__(self):
        self.mongo = api.mongo
        self.database = self.mongo['Users']
        self.collection = self.database['users']

    def __grab_users(self, jwt_token):
        try:
            # grab all user accounts from the database
            user_entries = self.collection.find({}, {
                "email": 1,
                "full_name": 1,
                "role": 1
            })

            # put user accounts on the backend
            user_accounts = [user for user in user_entries]

            json_response = {
                'status': 200,
                'users': user_accounts
            }

        except Exception as error:
            json_response = {
                'status': 400,
                'error': f'{error}'
            }

        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])

    def __hash_password(self, password):
        # hashes password and returns new password
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def handle_signin(self, data):
        return self.__signin(data)

    def handle_signup(self, data):
        return self.__signup(data) 

    def handle_grabbing_users(self, data):
        return self.__grab_users(data)

    def __signin(self, data):
        # check verify login
        if self.__verify_login(data['email'], data['password']):
            # grab user from database
            user = self.__user_exists(data['email'])

            # check if user is not None
            if user is not None:

                # construct response
                json_response = {
                    'status': 200,
                    'full_name': user['full_name'],
                    'role': user['role'],
                    'jwt_token': 'random_jwt_token'
                }

                return Response(json.dumps(json_response, default=json_util.default),
                                mimetype='application/json',
                                status=json_response['status'])

        # construct a negative json response 
        json_response = {
            'status': 400,
            'description': 'Invalid email/password combination'
        }

        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])

    def __signup(self, data):
        # check if user exists
        if self.__user_exists(data['email']) is None:
            # build new json
            user = {
                'email': data['email'],
                'password': self.__hash_password(data['password'].encode('utf-8')),
                'full_name': data['full_name'],
                'role': 'public'
            }

            # insert new user
            self.collection.insert_one(user)

            json_response = {
                'status': 201,
                'description': f'New {user["role"]} account was created!'
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
            return potential_user
        
        # could not find user
        return None 
    
    def __verify_login(self, email, password):
        potential_user = self.__user_exists(email)

        if potential_user:
            return self.__verify_password(password.encode('utf-8'), potential_user['password'])
        
        return False

    def __verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password, hashed_password)
