from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las
from api.errors.errors import *


class ApiAuthSignin(Resource):
    def post(self):
        response = las().handle_signin(request.json)
        return response

class ApiAuthToken(Resource):
    @jwt_required()
    def post(self):
        user_email = get_jwt_identity()

        response = las().handle_token_signin(user_email)

        return response
        