from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiAuthSignup(Resource):
    def post(self):
        '''
        Creates a user account

        @returns a response object
        '''

        response = las().handle_signup(request.json)
        return response