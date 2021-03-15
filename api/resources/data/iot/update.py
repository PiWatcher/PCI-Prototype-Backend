from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiDataIotUpdate(Resource):
    def post(self):
        json_body = request.json
        response = mms().insert_entry_by_room(json_body)
        return response