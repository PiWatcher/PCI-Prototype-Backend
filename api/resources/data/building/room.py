from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiDataBuildingRoomLive(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        params_dict = {'building_name': building_name, 'room': room}
        response = mms().get_live_data(params_dict)
        return response

class ApiDataBuildingRoomDaily(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        params_dict = {'building_name': building_name}
        response = mms().get_live_data(params_dict)
        return response

class ApiDataBuildingRoomWeekly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        params_dict = {'building_name': building_name, 'room': room}
        response = mms().get_weekly_data(params_dict)
        return response

class ApiDataBuildingRoomMonthly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        params_dict = {'building_name': building_name, 'room': room}
        response = mms().get_monthly_data(params_dict)
        return response

class ApiDataBuildingRoomQuarterly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        params_dict = {'building_name': building_name, 'room': room}
        response = mms().get_quarterly_data(params_dict)
        return response

class ApiDataBuildingRoomYearly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        params_dict = {'building_name': building_name, 'room': room}
        response = mms().get_yearly_data(params_dict)
        return response