import datetime
import json

from backend import mongo
from flask import jsonify, Response
from bson import json_util
class MongoService():

    def __init__(self):
        self.mongo = mongo

    def collect_all_entries_by_building(self, building):
        '''Collects all the entries in the building'''
        try:
            room_entries = []
            # grab the database
            database_object = self.mongo[building]

            collections = database_object.list_collections()

            for collection in collections:
                room_entries = room_entries + [entry for entry in database_object[collection['name']].find()]

            json_response = {
                "status": 200,
                "building": f'{building}',
                "data": room_entries
            }

            return Response(json.dumps(json_response, default=json_util.default), 
                            mimetype='application/json', 
                            status=200)

            # return json_response

        except Exception as error:
            json_response = {
                "status": 400,
                "error": f"{error}"
            }

            return Response(json.dumps(json_response), 
                            mimetype='application/json', 
                            status=400)

    def collect_all_entries_by_room(self, building, room):

        try:

            room_entries = []

            # grab the database
            database_object = self.mongo[building]

            collection_object = database_object[room]

            room_entries = room_entries + [entry for entry in collection_object.find()]

            json_response = {
                "status": 200,
                "building": f'{building}',
                "room": f'{room}',
                "data": room_entries
            }

            return Response(json.dumps(json_response, default=json_util.default), 
                            mimetype='application/json', 
                            status=200)

        except Exception as error:

            json_response = {
                "status": 400,
                "error": f"{error}"
            }

            return Response(json.dumps(json_response),
                            mimetype='application/json',
                            status=400)

    def insert_entry_by_room(self, data):
        '''Inserts a single entry into MongoDB''' 
        try:
            # append timestamp for the entry
            data["timestamp"] = datetime.datetime.now()

            # create a test database
            database_object = self.mongo[data["building"]]

            # create collection of entries for the endpoint
            collection_object = database_object[data["endpoint"]]

            # insert collection into collection
            collection_object.insert_one(data)

            # return the data back from the collection with success
            json_response = {
                        "status": 200,
                        "timestamp": data['timestamp'],
                        "message": f"[{data['building']} ({data['building_id']})] {data['endpoint']} ({data['endpoint_id']}) successfully added it's entry"
                   }

            return Response(json.dumps(json_response),
                            mimetype='application/json',
                            status=200)

        except Exception as error:

            json_response =  {
                        "status": 400, 
                        "error": f"{error}"
                   }

            return Response(json.dumps(json_response),
                            mimetype='application/json',
                            status=400)
    