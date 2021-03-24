from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiDataBuildingRooms(Resource):
    def get(self):
        json_body = request.json
        response = mms().collect_counts_of_rooms(json_body)
        return response