from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiDataBuildingRooms(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)

        response = mms().collect_counts_of_buildings(building_name)
        return response