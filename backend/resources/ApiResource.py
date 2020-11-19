import random
import datetime

from backend import app
from backend.services.MongoService import MongoService
from flask import request
from flask_restful import Resource, Api

class ApiBaseResource(Resource):
    def get(self):
        return {'data': {'success': 'Api base resource has been hit'}}

class ApiBuildingResource(Resource):
    def get(self, building):
        pass

class ApiEndpointResource(Resource):
    def get(self, building, endpoint, entries):
        pass
    
    def post(self):
        return MongoService().insert_entry(request.json)