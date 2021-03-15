from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiAuthUsers(Resource):
    def get(self):
        username = request.args.get('username', type=str)
        jwt_token = request.args.get('jwt_token', type=str)

        return jsonify({'status': 200, 'message': '/auth/users endpoint hit'})

class ApiAuthUsersUpdate(Resource):
    def post(self):
        username = request.args.get('username', type=str)
        jwt_token = request.args.get('jwt_token', type=str)
        json_body = request.json

        return jsonify({'status': 200, 'message': '/auth/users/update endpoint hit'})