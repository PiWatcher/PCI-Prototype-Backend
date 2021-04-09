from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiDataBuildingRooms(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        params_dict = {'building_name': building_name, 'room': room}
        response = mms().collect_counts_of_rooms(params_dict)
        return response