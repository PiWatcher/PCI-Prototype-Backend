import datetime

from backend import mongo
from flask import jsonify

class MongoService():

    def __init__(self):
        self.mongo = mongo

    def insert_entry(self, data):
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
            return {
                        "status": 200, 
                        "message": f"[{data['building']} ({data['building_id']})] {data['endpoint']} ({data['endpoint_id']}) successfully added it's entry at timestamp {data['timestamp']}"
                   }

        except Exception as error:
            return {
                        "status": 400, 
                        "message": f"Error: {error}"
                   }
