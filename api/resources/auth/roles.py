from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiAuthRoles(Resource):
    def get(self):
        jwt_token = request.args.get('jwt_token', type=str)

        # jwt_token communicates with service to check for valid login session

        response = las().handle_grabbing_roles()

        return response

    def post(self):
        jwt_token = request.args.get('jwt_token', type=str)
        json_body = request.json

        # jwt_token communicates with service to check for valid login session

        response = las().handle_creating_roles(json_body)

        return response