import random
import datetime

from backend import app
from backend.services import MongoService, RandomDataService
from flask_restful import Resource, Api

class ApiBaseResource(Resource):
    def get(self):
        return {'data': {'success': 'Api base resource has been hit'}}

class ApiBuidlingResource(Resource):
    def get(self, building):
        return {'data': {'building': f"{building}"}}

class ApiEndpointResource(Resource):
    def get(self, building, endpoint):

        random_count = random.randint(1, 10)
        current_time = datetime.datetime.now()

        return {'data': {'timestamp': f'{current_time}',
                         'building': f'building',
                         'endpoint': f'endpoint',
                         'count': random_count}}
    
    def post(self, building, endpoint):
        pass