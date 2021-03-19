from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiAuthUsers(Resource):
    def get(self):

        jwt_token = request.args.get('jwt_token', type=str)
        response = las().handle_grabbing_users(jwt_token)

        return response

class ApiAuthUsersUpdate(Resource):
    def post(self):
        jwt_token = request.args.get('jwt_token', type=str)
        json_body = request.json

        return jsonify({'status': 200, 'message': '/auth/users/update endpoint hit'})