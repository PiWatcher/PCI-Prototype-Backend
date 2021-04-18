
from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiAuthSignin(Resource):
    def post(self):
        response = las().handle_signin(request.json)
        return response