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
        self.users_collection = self.database['users']
        self.roles_collection = self.database['roles']

    def __construct_response(self, json_response):
        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])

    def __create_role(self, data):
        try:
            # check if role already exists
            if self.__grab_role(data['role_name']) is not None:
                # construct json object status: 409
                json_response = {
                    'status': 409,
                    'error': f'{data["role_name"]} already exists!'
                }
            else:
                # create role with new permission
                self.roles_collection.insert_one({
                    'role_name': data['role_name'],
                    'is_admin': data['is_admin'],
                    'can_view_raw': data['can_view_raw']
                })

                # grab the same role from the database
                new_role = self.__grab_role(data['role_name'])
                
                # construct json object with status: 200
                json_response = {
                    'status': 200,
                    'new_role': new_role
                }

        except Exception as error:
            json_response = {
                'status': 200,
                'error': f'{error}'
            }

        return self.__construct_response(json_response)

    def __grab_users(self):
        try:
            # grab all user accounts from the database
            user_entries = self.users_collection.find({}, {
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

        return self.__construct_response(json_response)

    def __grab_role(self, role_name):
        # attempt to grab role from database and return it
        return self.roles_collection.find_one({'role_name': role_name})

    def __grab_roles(self):
        try:
            # grab all entries from the roles collections
            roles_entries = self.roles_collection.find()

            # construct list of roles
            roles = [role for role in roles_entries]

            # construct json response
            json_response = {
                'status': 200,
                'roles': roles
            }

        except Exception as error:
            json_response = {
                'status': 400,
                'error': f'{error}'
            }

        # create and send resposne
        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])

    def __hash_password(self, password):
        # hashes password and returns new password
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def handle_creating_roles(self, data):
        return self.__create_role(data)

    def handle_grabbing_users(self):
        return self.__grab_users()

    def handle_grabbing_roles(self):
        return self.__grab_roles()

    def handle_signin(self, data):
        return self.__signin(data)

    def handle_signup(self, data):
        return self.__signup(data) 

    def handle_updating_user(self, data):
        return self.__update_user(data)

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
            self.users_collection.insert_one(user)

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
        potential_user = self.users_collection.find_one({'email': email})

        # if user exists
        if potential_user:
            return potential_user
        
        # could not find user
        return None 

    def __update_user(self, data):
        try:
            email = data["email"]
            new_role = data["new_role"]

            # update document with new role
            self.users_collection.update_one({"email": email}, {"$set": {"role": new_role}})
            user = self.users_collection.find_one({"email": email})

            json_response = {
                'status': 200,
                'user': {
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'role': user['role']
                }
            }
        except Exception as error:
            json_response = {
                'status': 400,
                'error': f'{error}'
            }
        
        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])
    
    def __verify_login(self, email, password):
        potential_user = self.__user_exists(email)

        if potential_user:
            return self.__verify_password(password.encode('utf-8'), potential_user['password'])
        
        return False

    def __verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password, hashed_password)
