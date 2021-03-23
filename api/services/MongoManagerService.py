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

    def collect_counts_of_rooms(self, query_filter={}):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building_name"]
            collection = database_object[building]
            
            room_list = collection.distinct("endpoint")
            
            rooms_and_counts = collection.aggregate([{$group: {_id: "$endpoint", current_count: {$last: "$count"}}}])

            for one_room in rooms_and_counts:
                for room, count in one_room:
                    total_count = count
                
            total_room = len(rooms_and_counts)

            json_response = {
                'status': 200,
                'room_total': total_room,
                'count_total': total_count,
                'data': rooms_and_counts
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

###############################################################################
########################Periodic Data Pulls####################################
###############################################################################
    def get_live_data(self, query_filter={}):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building_name"]
            room = query_filter["room"]
            collection = database_object[building]
            
            room_list = collection.distinct("endpoint")
            
            live_room_counts = db.Egr.aggregate(     
                {$match:{"endpoint":room}},
                {$limit: 720},
                {$group: { _id:"$endpoint", total_count:{$sum:"$count"}}})

            json_response = {
                'status': 200,
                'data': live_room_counts
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

    def get_daily_data(self, query_filter={}):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building_name"]
            room = query_filter["room"]
            collection = database_object[building]
            
            room_list = collection.distinct("endpoint")
            
            for skip_index in range(0, 61):
                skip_count = skip_index * 288
                live_room_counts = db.Egr.aggregate(
                    {$match:{"endpoint":room}},
                    {$skip: skip_count}
                    {$limit: 288},
                    {$group: { _id:"$endpoint", total_count:{$sum:"$count"}}})


            json_response = {
                'status': 200,
                'data': live_room_counts
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

    def get_weekly_data(self, query_filter={}):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building_name"]
            room = query_filter["room"]
            collection = database_object[building]
            
            room_list = collection.distinct("endpoint")
            
            for skip_index in range(0, 169):
                skip_count = skip_index * 720
                live_room_counts = db.Egr.aggregate(
                    {$match:{"endpoint":room}},
                    {$skip: skip_count}
                    {$limit: 720},
                    {$group: { _id:"$endpoint", total_count:{$sum:"$count"}}})

            json_response = {
                'status': 200,
                'data': live_room_counts
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

    def get_monthly_data(self, query_filter={}):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building_name"]
            room = query_filter["room"]
            collection = database_object[building]
            
            room_list = collection.distinct("endpoint")
            
            for skip_index in range(0, 731):
                skip_count = skip_index * 720
                live_room_counts = db.Egr.aggregate(
                    {$match:{"endpoint":room}},
                    {$skip: skip_count}
                    {$limit: 720},
                    {$group: { _id:"$endpoint", total_count:{$sum:"$count"}}})

            json_response = {
                'status': 200,
                'data': live_room_counts
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

    def get_quarterly_data(self, query_filter={}):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building_name"]
            room = query_filter["room"]
            collection = database_object[building]
            
            room_list = collection.distinct("endpoint")
            
            for skip_index in range(0, 93):
                skip_count = skip_index * 17280
                live_room_counts = db.Egr.aggregate(
                    {$match:{"endpoint":room}},
                    {$skip: skip_count}
                    {$limit: 17280},
                    {$group: { _id:"$endpoint", total_count:{$sum:"$count"}}})

            json_response = {
                'status': 200,
                'data': live_room_counts
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

    def get_yearly_data(self, query_filter={}):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building_name"]
            room = query_filter["room"]
            collection = database_object[building]
            
            room_list = collection.distinct("endpoint")
            
            for skip_index in range(0, 369):
                skip_count = skip_index * 17280
                live_room_counts = db.Egr.aggregate(
                    {$match:{"endpoint":room}},
                    {$skip: skip_count}
                    {$limit: 17280},
                    {$group: { _id:"$endpoint", total_count:{$sum:"$count"}}})

            json_response = {
                'status': 200,
                'data': live_room_counts
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

