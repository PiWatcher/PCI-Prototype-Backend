import api
import json
import datetime
import random

from flask import Response
from bson import json_util

class MongoManagerService():

    def __init__(self):
        self.mongo = api.mongo
    
    def collect_all_buildings(self):
        try:
            database_object = self.mongo["Buildings"]
            buildings = database_object.list_collection_names()

            json_response = {
                'status': 200,
                'data': buildings
            }

            return Response(json.dumps(json_response, default=json_util.default),
                            mimetype='application/json',
                            status=200)

        except Exception as error:
            json_response = {
                'status': 400,
                'error': f'{error}'
            }

            return Response(json.dumps(json_response,
                            mimetype='application/json',
                            status=400))

    def collect_all_entries_by_building(self, building, query_filter={}):
        try:
            room_entries = []
            database_object = self.mongo["Buildings"]
            collection = database_object[building]

            entries = collection.find(query_filter)
            room_entries = [entry for entry in entries]

            json_response = {
                'status': 200,
                'building': f'{building}',
                'data': room_entries
            }

            return Response(json.dumps(json_response, default=json_util.default),
                            mimetype='application/json',
                            status=200)

        except Exception as error:
            json_response = {
                'status': 400,
                'error': f'{error}'
            }

            return Response(json.dumps(json_response),
                            mimetype='application/json',
                            status=400)

    def insert_entry_by_room(self, data):
        try:
            database_object = self.mongo["Buildings"]
            collection_object = database_object[data["building"]]
            collection_object.insert_one(data)

            json_response = {
                'status': 200,
                'timestamp': data['timestamp'],
                'message': f"[{data['building']} ({data['building_id']})] {data['endpoint']} ({data['endpoint_id']}) successfully added it's entry"
            }

            return Response(json.dumps(json_response, default=json_util.default),
                            mimetype='application/json',
                            status=200)

        except Exception as error:
            json_response = {
                'status': 400,
                'error': f'{error}'
            }

            return Response(json.dumps(json_response),
                            mimetype='application/json',
                            status=400)
    
    def mock_data_entry(self, building, iterations=10):

        for iteration in range(0, iterations):
            self.insert_entry_by_room(self.__prepare_mock_data(building, iterations))

        json_response = {
            'status': 200,
            'message': f'{iterations} entries of mock data was inserted into {building.capitalize()}'
        }
        
        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])
    
    def __prepare_mock_data(self, building, iterations):
        data = {}
        random_room = random.randint(100, 150)
        random_endpoint_id = random.randint(1,4)
        random_count = random.randint(1, 50)

        data['timestamp'] = datetime.datetime.now()
        data['building'] = building.capitalize()
        data['building_id'] = 1
        data['count'] = random_count
        data['endpoint'] = f'Room {random_room}'
        data['endpoint_id'] = f'EPID_{random_endpoint_id}'
        data['room_capacity'] = 50

        return data