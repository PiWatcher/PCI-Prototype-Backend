from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiAuthUsers(Resource):
    def get(self):
        jwt_token = request.args.get('jwt_token', type=str)

        # jwt_token is used to check permissions

        response = las().handle_grabbing_users()

        return response
    
    def delete(self):
        jwt_token = request.args.get('jwt_token', type=str)
        json_body = request.json

        # jwt_token to check permissions
        
        response = las().handle_deleting_user(json_body)

        return response

class ApiAuthUsersUpdate(Resource):
    def post(self):
        jwt_token = request.args.get('jwt_token', type=str)
        json_body = request.json

        # jwt_token is used to check permissions

        response = las().handle_updating_user_role(json_body)

        return response

class ApiAuthUsersUpdatePassword(Resource):
    def post(self):
        json_body = request.json

        response = las().handle_updating_password(json_body)

        return response