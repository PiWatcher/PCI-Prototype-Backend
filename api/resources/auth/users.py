from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las
from api.errors.errors import *

class ApiAuthUsers(Resource):
    @jwt_required()
    def get(self):
        user_email = get_jwt_identity()

        if las().validate_permission(user_email):
            response = las().handle_grabbing_users()
        else:
            response = las().construct_response(errors["BadTokenError"])

        return response
    
    @jwt_required()
    def delete(self):
        user_email = get_jwt_identity()

        if las().validate_permission(user_email):
            json_body = request.json
            response = las().handle_deleting_user(json_body)
        else:
            response = las().construct_response(errors["BadTokenError"])

        return response

class ApiAuthUsersUpdate(Resource):
    @jwt_required()
    def post(self):
        user_email = get_jwt_identity()

        if las().validate_permission(user_email):
            json_body = request.json
            response = las().handle_updating_user_role(json_body)
        else:
            response = las().construct_response(errors["BadTokenError"])

        return response

class ApiAuthUsersUpdatePassword(Resource):
    def post(self):

        json_body = request.json
        response = las().handle_updating_password(json_body)

        return response