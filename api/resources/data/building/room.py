from datetime import *
from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiDataBuildingRoomLive(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)

        response = mms().get_live_data(building_name, room)
        return response

class ApiDataBuildingRoomDaily(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)

        response = mms().get_daily_data(building_name, room)
        return response

class ApiDataBuildingRoomWeekly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)

        response = mms().get_weekly_data(building_name, room)
        return response

class ApiDataBuildingRoomMonthly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)

        response = mms().get_monthly_data(building_name, room)
        return response

class ApiDataBuildingRoomQuarterly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)

        response = mms().get_quarterly_data(building_name, room)
        return response

class ApiDataBuildingRoomYearly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)

        response = mms().get_yearly_data(building_name, room)
        return response