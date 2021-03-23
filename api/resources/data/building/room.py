from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiDataBuildingRoomLive(Resource):
    def get(self):
        json_body = request.json
        response = get_live_data(json_body)
        return response

class ApiDataBuildingRoomDaily(Resource):
    def get(self):
        json_body = request.json
        response = get_live_data(json_body)
        return response

class ApiDataBuildingRoomWeekly(Resource):
    def get(self):
        json_body = request.json
        response = get_weekly_data(json_body)
        return response

class ApiDataBuildingRoomMonthly(Resource):
    def get(self):
        json_body = request.json
        response = get_monthly_data(json_body)
        return response

class ApiDataBuildingRoomQuarterly(Resource):
    def get(self):
        json_body = request.json
        response = get_quarterly_data(json_body)
        return response

class ApiDataBuildingRoomYearly(Resource):
    def get(self):
        json_body = request.json
        response = get_yearly_data(json_body)
        return response