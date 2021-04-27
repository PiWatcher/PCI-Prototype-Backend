from flask import jsonify, request
from flask_restful import Resource

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiDataBuildings(Resource):
    def get(self):
        '''
        Gets the list of buildings that have entries in the database

        @returns a response object
        '''

        response = mms().collect_all_buildings()
        return response