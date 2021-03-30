from datetime import *
from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiDataBuildingRoomLive(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        current_time = str(datetime.now())
        interval = str(datetime.now() - timedelta(minutes = 5))
        params_dict = {'timestamp': {'$lte': current_time, '$gte': interval} ,'building': building_name, 'endpoint': room}
        response = mms().get_live_data(params_dict, current_time)
        return response

class ApiDataBuildingRoomDaily(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        current_time = datetime.now()
        interval = datetime.now() - timedelta(minutes = 5)

        params_dict = {'timestamp': {'$lte': current_time, '$gte': interval},'building': building_name, 'endpoint': room}
        response = mms().get_daily_data(params_dict, current_time)
        return response

class ApiDataBuildingRoomWeekly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        current_time = datetime.now()
        interval = datetime.now() - timedelta(minutes = 5)

        params_dict = {'timestamp': {'$lte': current_time, '$gte': interval},'building': building_name, 'endpoint': room}
        response = mms().get_weekly_data(params_dict, current_time)
        return response

class ApiDataBuildingRoomMonthly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        current_time = datetime.now()
        interval = datetime.now() - timedelta(minutes = 5)

        params_dict = {'timestamp': {'$lte': current_time, '$gte': interval},'building': building_name, 'endpoint': room}
        response = mms().get_monthly_data(params_dict, current_time)
        return response

class ApiDataBuildingRoomQuarterly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        current_time = datetime.now()
        interval = datetime.now() - timedelta(minutes = 5)

        params_dict = {'timestamp': {'$lte': current_time, '$gte': interval},'building': building_name, 'endpoint': room}
        response = mms().get_quarterly_data(params_dict, current_time)
        return response

class ApiDataBuildingRoomYearly(Resource):
    def get(self):
        building_name = request.args.get('building_name', type=str)
        room = request.args.get('room', type=str)
        current_time = datetime.now()
        interval = datetime.now() - timedelta(minutes = 5)

        params_dict = {'timestamp': {'$lte': current_time, '$gte': interval},'building': building_name, 'endpoint': room}
        response = mms().get_yearly_data(params_dict, current_time)
        return response