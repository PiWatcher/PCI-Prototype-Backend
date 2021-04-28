from api.services.BaseService import BaseService
from api.models.AccountModel import Account
from api.models.RoleModel import Role
from api.errors.errors import *
from flask_jwt_extended import create_access_token

import datetime

class LoginAuthenticationService(BaseService):

    def handle_creating_roles(self, data):
        '''
        A public handler function for creating roles

        @returns a response object for creating a role
        '''

        return self.__create_role(data)

    def handle_deleting_role(self, data):
        '''
        A public handler function for deleting roles

        @returns a response object for deleting a role 
        '''

        return self.__delete_role(data)

    def handle_deleting_user(self, data):
        '''
        A public handler function for deleting a user

        @returns a response object for deleting a role
        '''

        return self.__delete_user(data)

    def handle_grabbing_users(self):
        '''
        A public handler function for grabbing users

        @returns a response object for grabbing users
        '''

        return self.__grab_users()

    def handle_grabbing_roles(self):
        '''
        A public handler function for grabbing roles

        @returns a response object for grabbing roles
        '''

        return self.__grab_roles()

    def handle_signin(self, data):
        '''
        A public handler function for signing to an account

        @returns a response object for the signed in user
        '''

        return self.__signin(data)

    def handle_token_signin(self, data):
        '''
        A public handler function for signing with a user token

        @returns a response object for the signed in user
        '''

        return self.__token_signin(data)

    def handle_signup(self, data):
        '''
        A public handler function for signing up for a user account

        @returns a response object for a signed up account
        '''
        return self.__signup(data) 

    def handle_updating_user_role(self, data):
        '''
        A public handler function for updating a user's role

        @returns a response object for the updated user
        '''

        return self.__update_user_role(data)

    def handle_updating_password(self, email, data):
        '''
        A public handler function for updating a user's password

        @returns a response object for the updated user
        '''

        return self.__update_user_password(email, data)

    def validate_permission(self, email):
        '''
        Validates a users permission to access the admin dashboard

        @return a boolean value
        '''

        potential_user = self.__grab_user(email)
        user_role = self.__grab_role(potential_user["role"])

        if user_role['is_admin']:
            return True
        
        return False

    def __create_role(self, data):
        '''
        Creates a new role in the database

        @raises RoleAlreadyExistsError if that role already exists

        @return a response object
        '''

        try:
            # check if role already exists
            if self.__grab_role(data['role_name']) is not None:
                raise RoleAlreadyExistsError

            # create new role in the database
            super().get_database('Users')['roles'].insert_one(
                Role(**data).to_json()
            )

            # grab the same role from the database
            new_role = self.__grab_role(data['role_name'])

            # if role does not exist
            if new_role is None:
                # raise FailedRoleCreationError
                raise InternalServerError

            # construct successful response 
            return super().construct_response({
                'status': 200,
                'new_role': new_role
            })

        except RoleAlreadyExistsError:
            return super().construct_response(errors["RoleAlreadyExistsError"])

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def __delete_role(self, data):
        '''
        Deletes a role from the database

        @raises SchemaValidationError if the schema does not contain the correct keys
        @raises RoleDoesNotExistError if the role does not exist
        
        @returns a response object
        '''

        try:
            # grab roles from data
            role_name = data.get("role_name", None)

            # Validate schema
            if role_name is None:
                raise SchemaValidationError

            # grab role from mongo database
            role = self.__grab_role(role_name)

            # check if role exists
            if role is None:
                raise RoleDoesNotExistError
            
            # delete role from database
            super().get_database("Users")["roles"].delete_one({
                "role_name": role_name
            })

            # check if role is still in database
            if self.__grab_role(role_name) is not None:
                raise FailedRoleDeletionError
            
            return super().construct_response({
                'status': 200,
                'message': f'Successfully deleted {role_name} from roles.'
            })
        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except RoleDoesNotExistError:
            return super().construct_response(errors["RoleDoesNotExistError"])
        except FailedRoleDeletionError:
            return super().construct_response(errors["FailedRoleDeletionError"])
        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def __delete_user(self, data):
        '''
        Deletes a user from the database

        @raises SchemaValidationError if the schema is missing a required key
        @raises EmailDoesNotExistError if the email does not exist in the database

        @returns a response object
        '''

        try:
            # grab email from data
            email = data.get("email", None)

            # validate schema
            if email is None:
                raise SchemaValidationError

            # grab user from database
            user = self.__grab_user(email)

            # check if user exists
            if user is None:
                raise EmailDoesNotExistError

            # delete user from database
            super().get_database("Users")["users"].delete_one({
                "email": email
            })

            # check if user is still in database
            if self.__grab_user(email) is not None:
                raise FailedUserDeletionError
            
            return super().construct_response({
                'status': 200,
                'message': f'Successfully deleted {email} from database'
            })
        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except EmailDoesNotExistError:
            return super().construct_response(errors["EmailDoesNotExistError"])
        except FailedUserDeletionError:
            return super().construct_response(errors["FailedUserDeletionError"])
        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def __grab_user(self, email):
        '''
        Grabs a single user from the mongodb database

        @param email used to query for a single user

        @returns the potential user that is grabbed from the database
        '''

        # find user in the database by email
        potential_user = super().get_database('Users')['users'].find_one({
            "email": email
            }, {"_id": 0})

        # if user exists
        if potential_user:
            return potential_user
        
        # could not find user
        return None 

    def __grab_users(self):
        '''
        Grabs all the users from the mongodb database

        @returns a response object
        '''
        try:
            # grab all user accounts from the database
            user_entries = super().get_database("Users")["users"].find({}, {
                "_id": 0,
                "email": 1,
                "full_name": 1,
                "role": 1
            })

            # put user accounts on the backend
            user_accounts = [user for user in user_entries]

            # construct successful response
            return super().construct_response({
                'status': 200,
                'users': user_accounts
            })

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def __grab_role(self, role_name):
        '''
        Grabs a role by role name from the database

        @param role_name the role to be grabbed from the database

        @return the role from the database
        '''
        # attempt to grab role from database and return it
        return super().get_database("Users")["roles"].find_one({
            'role_name': role_name
            }, {"_id": 0})

    def __grab_roles(self):
        '''
        Grabs all roles that are defined in the database

        @returns a response object
        '''

        try:
            # grab all entries from the roles collections
            roles_entries = super().get_database("Users")["roles"].find({}, {"_id": 0})

            # construct list of roles
            roles = [role for role in roles_entries]

            # construct successful response
            return super().construct_response({
                'status': 200,
                'roles': roles
            })

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def __signin(self, data):
        '''
        Functionality for signing into an account

        @param data a json object that contains the email and password
                    for an account

        @raises SchemaValidationError if it is missing required fields

        @returns a response object
        '''

        try:
            email = data.get("email", None)
            password = data.get("password", None)

            if email is None:
                raise SchemaValidationError

            if password is None:
                raise SchemaValidationError

            # check verify login
            if self.__verify_login(email, password):
                # grab user from database
                user = self.__grab_user(email)

                # construct JWT token
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(identity=user['email'],
                                                   expires_delta=expires)

                role = self.__grab_role(user['role'])

                # successful response
                return super().construct_response({
                    'status': 200,
                    'full_name': user['full_name'],
                    'role': role,
                    'jwt_token': access_token
                })
            else:
                raise UnauthorizedError

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except UnauthorizedError:
            return super().construct_response(errors["UnauthorizedError"])
        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def __signup(self, data):
        '''
        Functionality for creating a user account in the database

        @param data json object the contains the required fields

        @raises SchemaValidationError if it is missing required fields
        @raises EmailAlreadyExistsError if an account already has that email

        @returns a response object
        '''

        try:
            email = data.get("email", None)
            password = data.get("password", None)
            full_name = data.get("full_name", None)

            if email is None:
                raise SchemaValidationError
            
            if password is None:
                raise SchemaValidationError

            if full_name is None:
                raise SchemaValidationError

            # check if user exists
            user = self.__grab_user(email)

            # raise error if user already exists
            if user is not None:
                raise EmailAlreadyExistsError

            # insert new account
            super().get_database('Users')['users'].insert_one(
                Account(**data).hash_password().to_json()
            )

            # check if account in database
            user = self.__grab_user(email)

            # if user was not created
            if user is None:
                # raise FailedUserCreationError
                raise InternalServerError

            # construct successful response
            return super().construct_response({
                'status': 201,
                'message': f'New {user["role"]} account was created!'
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except EmailAlreadyExistsError:
            return super().construct_response(errors['EmailAlreadyExistsError'])
        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)
        
    def __token_signin(self, data):
        '''
        Functionality for signing in with a user/jwt token

        @param data the email used to grab a user

        @raises EmailDoesNotExistError if the email does not exist

        @returns a response object
        '''

        try: 
            user = self.__grab_user(data)

            if user is None:
                raise EmailDoesNotExistError
            
            role = self.__grab_role(user['role'])

            return super().construct_response({
                'status': 200,
                'full_name': user['full_name'],
                'role': role,
            })
        
        except EmailDoesNotExistError:
            return super().construct_response(errors["EmailDoesNotExistError"])
        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def __update_user_role(self, data):
        '''
        Updates a users role in the database

        @param data contains the required keys for updating a user role

        @raises SchemaValidationError if the data is missing required fields
        @raises RoleDoesNotExistError if the role does not exist in the database

        @returns a response object
        '''

        try:
            email = data.get('email', None)
            new_role = data.get('new_role', None)

            if email is None:
                raise SchemaValidationError

            if new_role is None:
                raise SchemaValidationError

            # check if user exists
            user = self.__grab_user(email)

            # raise error if user does not exist
            if user is None:
                raise EmailDoesNotExistError

            # check if new role exists
            role = self.__grab_role(new_role)

            # raise error if role does not exist
            if role is None:
                raise RoleDoesNotExistError

            # update document with new role
            super().get_database('Users')['users'].update_one(
                {"email": email},
                {"$set": {"role": new_role}}
            )

            # grab updated user
            user = self.__grab_user(email)

            # check if user
            if user is None:
                raise InternalServerError

            # construct successful response
            return super().construct_response({
                'status': 200,
                'user': {
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'role': user['role']
                }
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except EmailDoesNotExistError:
            return super().construct_response(errors["EmailDoesNotExistError"])
        except RoleDoesNotExistError:
            return super().construct_response(errors["RoleDoesNotExistError"])
        except (InternalServerError, Exception):
            return super().construct_response(errors["InternalServerError"])

    def __update_user_password(self, email, data):
        '''
        Updates a user's password in the database

        @param data the required keys for updating the user password

        @raises SchemaValidationError if the data is missing required keys
        @raises UnauthorizedError if the account failed to authorize

        @returns a response object
        '''

        try:
            # validate schema of data
            password = data.get("password", None)
            new_password = data.get("new_password", None)

            # validate email is there
            if email is None:
                raise SchemaValidationError

            if password is None:
                raise SchemaValidationError
            
            if new_password is None:
                raise SchemaValidationError

            # search for user in database
            user = self.__grab_user(email)

            # raise error is user does not exist
            if user is None:
                raise EmailDoesNotExistError

            # create current account
            if not Account(**user).check_password_hash(password):
                raise UnauthorizedError

            # create a new account with new password
            updated_user = Account(
                email=user["email"],
                password=new_password,
                full_name=user["full_name"],
                role=user["role"]
            ).hash_password()

            # update user in database
            super().get_database('Users')['users'].update_one(
                {"email": email},
                {"$set": {"password": updated_user.get_password()}}
            )

            # create response object
            return super().construct_response({
                'status': 200,
                'description': f'{updated_user.get_email()} password was updated'
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except UnauthorizedError:
            return super().construct_response(errors["UnauthorizedError"])
        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message['error'] = f'{error}'
            return super().construct_response(error_message)
        
    def __verify_login(self, email, password):
        '''
        Verify a users login by validating the user with an email/password

        @param email the key to search the user by
        @param password the password to check upon

        @returns a boolean value
        '''

        potential_user = self.__grab_user(email)

        if potential_user:
            return Account(**potential_user).check_password_hash(password)
        
        return False
