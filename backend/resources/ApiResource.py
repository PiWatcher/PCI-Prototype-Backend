import random
import datetime

from backend import app
from backend.services import MongoService
from flask_restful import Resource, Api

class ApiBaseResource(Resource):
    def get(self):
        return {'data': {'success': 'Api base resource has been hit'}}

class ApiBuidlingResource(Resource):
    def get(self, building):
        return {'data': {'building': f"{building}"}}

class ApiEndpointResource(Resource):
    def get(self, building, endpoint):

        building_map = {'90': 'SICCS'}

        room_map = {'100': 'Main Lobby'}

        random_count = random.randint(1, 10)
        current_time = datetime.datetime.now()

        return {'data': {'timestamp': f'{current_time}',
                         'building_id': f'{building}',
                         'building_name': f'{building_map[building]}',
                         'endpoint_id': f'{endpoint}',
                         'endpoint_name': f'{room_map[endpoint]}',
                         'count': random_count}}
    
    def post(self, building, endpoint):
        pass