from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las
from api.errors.errors import *

class ApiAuthRoles(Resource):
    @jwt_required()
    def get(self):
        '''
        Gets all roles from the database.

        @returns a response object
        '''

        user_email = get_jwt_identity()

        if las().validate_permission(user_email):
            response = las().handle_grabbing_roles()
        else:
            response = las().construct_response(errors["BadTokenError"])

        return response

    @jwt_required()
    def post(self):
        '''
        Creates a role in the database

        @returns a response object
        '''

        user_email = get_jwt_identity()

        if las().validate_permission(user_email):
            json_body = request.json
            response = las().handle_creating_roles(json_body)
        else:
            response = las().construct_response(errors["BadTokenError"])

        return response

    @jwt_required()
    def delete(self):
        '''
        Deletes a role from the database

        @returns a response object
        '''

        user_email = get_jwt_identity()

        if las().validate_permission(user_email):
            json_body = request.json
            response = las().handle_deleting_role(json_body)
        else:
            response = las().construct_response(errors["BadTokenError"])

        return response