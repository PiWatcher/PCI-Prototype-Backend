from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiAuthSignout(Resource):
    def get(self):
        json_body = request.json

        return None