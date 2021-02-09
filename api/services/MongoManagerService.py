import api
import json
import datetime

from flask import Response
from bson import json_util

class MongoManagerService():

    def __init__(self):
        self.mongo = api.mongo
    
    def collect_all_buildings(self):
        try:
            json_response = {
                'status': 200,
                'data': self.mongo.list_database_names()
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

    def collect_all_entries_by_building(self, building):
        try:
            room_entries = []
            database_object = self.mongo[building]
            collections = database_object.list_collections()

            for collection in collections:
                room_entries = room_entries + [entry for entry in database_object[collection['name']].find()]

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
            database_object = self.mongo[data["building"]]
            collection_object = database_object[data["endpoint"]]
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