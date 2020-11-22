import random
import datetime

from backend import app
from backend.services.MongoService import MongoService
from flask import request
from flask_restful import Resource, Api

class ApiBaseResource(Resource):

    def get(self):
        return {'status': 200,'message': 'Api base resource has been hit'}

class ApiBuildingResource(Resource):
    '''A resource that gathers all entry information for every single endpoint from a particular building'''

    def get(self, building):
        response = MongoService().collect_all_entries_by_building(building)
        return response

class ApiRoomResource(Resource):
    '''A resource that gathers all entry information from a particular endpoint from a particular building'''

    def get(self, building, room):
        response = MongoService().collect_all_entries_by_room(building, room)
        return response
    
class ApiUpdateResource(Resource):
    '''A resource for providing endpoints a place to submit their entries into the database'''

    def post(self):
        response = MongoService().insert_entry_by_room(request.json)
        return response
