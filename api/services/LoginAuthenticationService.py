from api.services.BaseService import BaseService
from api.models.AccountModel import Account
from api.models.RoleModel import Role
from api.errors.errors import *

class LoginAuthenticationService(BaseService):

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

    def handle_updating_user_role(self, data):
        return self.__update_user_role(data)

    def __create_role(self, data):
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

    def __grab_user(self, email):
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
        # attempt to grab role from database and return it
        return super().get_database("Users")["roles"].find_one({
            'role_name': role_name
            }, {"_id": 0})

    def __grab_roles(self):
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
        try:
            # check verify login
            if self.__verify_login(data['email'], data['password']):
                # grab user from database
                user = self.__grab_user(data['email'])

                # check if user exists
                if user is None:
                    raise EmailDoesNotExistError

                role = self.__grab_role(user['role'])

                # successful response
                return super().construct_response({
                    'status': 200,
                    'full_name': user['full_name'],
                    'role': role,
                    'jwt_token': 'random_jwt_token'
                })
            else:
                raise UnauthorizedError

        except UnauthorizedError:
            return super().construct_response(errors["UnauthorizedError"])
        except EmailDoesNotExistError:
            return super().construct_response(errors["EmailDoesNotExistError"])
        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def __signup(self, data):
        try:
            # check if user exists
            user = self.__grab_user(data['email'])

            # raise error if user already exists
            if user is not None:
                raise EmailAlreadyExistsError

            # insert new account
            super().get_database('Users')['users'].insert_one(
                Account(**data).hash_password().to_json()
            )

            # check if account in database
            user = self.__grab_user(data['email'])

            # if user was not created
            if user is None:
                # raise FailedUserCreationError
                raise InternalServerError

            # construct successful response
            return super().construct_response({
                'status': 201,
                'message': f'New {user["role"]} account was created!'
            })

        except EmailAlreadyExistsError:
            return super().construct_response(errors['EmailAlreadyExistsError'])
        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)
        
    def __update_user_role(self, data):
        try:
            # check if user exists
            user = self.__grab_user(data['email'])

            # raise error if user does not exist
            if user is None:
                raise EmailDoesNotExistError

            # check if new role exists
            role = self.__grab_role(data['new_role'])

            # raise error if role does not exist
            if role is None:
                raise RoleDoesNotExistError

            # update document with new role
            super().get_database('Users')['users'].update_one(
                {"email": data['email']},
                {"$set": {"role": data['new_role']}}
            )

            # grab updated user
            user = self.__grab_user(data['email'])

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

        except EmailDoesNotExistError:
            return super().construct_response(errors["EmailDoesNotExistError"])
        except RoleDoesNotExistError:
            return super().construct_response(errors["RoleDoesNotExistError"])
        except (InternalServerError, Exception):
            return super().construct_response(errors["InternalServerError"])
    
    def __verify_login(self, email, password):

        potential_user = self.__grab_user(email)

        if potential_user:
            return Account(**potential_user).check_password_hash(password)
        
        return False