import api
import json
from datetime import timedelta, datetime
import math
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
            rooms_and_counts_list = []
            rooms_and_counts = {}
            total_count = 0
            
            rooms_and_counts_cursor = collection.aggregate([{"$group": {"_id": "$endpoint", "current_count": {"$last": "$count"}}}])

            for item in rooms_and_counts_cursor:
                rooms_and_counts[item["_id"]]= item["current_count"]
                rooms_and_counts_list.append(item)
                
            total_room = len(rooms_and_counts)

            for room in rooms_and_counts:
                total_count += rooms_and_counts[room]

            json_response = {
                'status': 200,
                'data': rooms_and_counts_list
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

        data['timestamp'] = datetime.now()
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
    def get_live_data(self, query_filter, current_time):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building"]
            collection = database_object[building]
            time_offset = 0
            total_count = 0
            daily_counts = []
            json_str = []
            entry_offset = 720

            

            
            endpoint_total = len(collection.find(query_filter).distinct('endpoint_id'))
            
            live_room_counts_cursor = collection.find(query_filter).limit(entry_offset)

            for item in live_room_counts_cursor:
                temp_dict = {}
                temp_dict['timestamp'] = item['timestamp']
                temp_dict['count'] = item['count']
                json_str.append(temp_dict)

            json_response = {
                'status': 200,
                'data': json_str
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

    def get_daily_data(self, query_filter, current_time):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building"]
            collection = database_object[building]
            daily_counts = []
            

            entry_offset = 288
            time_offset = 60
            

            endpoints = collection.find(query_filter).distinct('endpoint_id')

            endpoint_total = len(endpoints)
            
            for skip_index in range(0, 61):
                new_time_offset = time_offset * skip_index
                segmented_counts = []
                skip_count = skip_index * entry_offset
                daily_room_cursor = collection.find(query_filter).skip( skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

                for item in daily_room_cursor:
                    segmented_counts.append(item['count'])
                    
                daily_counts.append(self.__average_counts_by_time(segmented_counts, current_time, new_time_offset, endpoint_total))




            json_response = {
                'status': 200,
                'data': daily_counts
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

    def get_weekly_data(self, query_filter, current_time):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building"]
            collection = database_object[building]
            weekly_counts = []
            

            entry_offset = 720
            time_offset = 60
            

            endpoints = collection.find(query_filter).distinct('endpoint_id')

            endpoint_total = len(endpoints)
            
            for skip_index in range(0, 169):
                new_time_offset = time_offset * skip_index
                segmented_counts = []
                skip_count = skip_index * entry_offset
                weekly_room_cursor = collection.find(query_filter).skip( skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

                for item in weekly_room_cursor:
                    segmented_counts.append(item['count'])
                    
                weekly_counts.append(self.__average_counts_by_time(segmented_counts, current_time, new_time_offset, endpoint_total))

            json_response = {
                'status': 200,
                'data': weekly_counts
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

    def get_monthly_data(self, query_filter, current_time):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building"]
            collection = database_object[building]
            monthly_counts = []
            

            entry_offset = 720
            time_offset = 60
            

            endpoints = collection.find(query_filter).distinct('endpoint_id')

            endpoint_total = len(endpoints)
            
            for skip_index in range(0, 731):
                new_time_offset = time_offset * skip_index
                segmented_counts = []
                skip_count = skip_index * entry_offset
                monthly_room_cursor = collection.find(query_filter).skip( skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

                for item in monthly_room_cursor:
                    segmented_counts.append(item['count'])
                    
                monthly_counts.append(self.__average_counts_by_time(segmented_counts, current_time, new_time_offset, endpoint_total))

            json_response = {
                'status': 200,
                'data': monthly_counts
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

    def get_quarterly_data(self, query_filter, current_time):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building"]
            collection = database_object[building]
            quarterly_counts = []
            

            entry_offset = 17280
            time_offset = 1440
            

            endpoints = collection.find(query_filter).distinct('endpoint_id')

            endpoint_total = len(endpoints)
            
            for skip_index in range(0, 93):
                new_time_offset = time_offset * skip_index
                segmented_counts = []
                skip_count = skip_index * entry_offset
                quarterly_room_cursor = collection.find(query_filter).skip( skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

                for item in quarterly_room_cursor:
                    segmented_counts.append(item['count'])
                    
                quarterly_counts.append(self.__average_counts_by_time(segmented_counts, current_time, new_time_offset, endpoint_total))

            json_response = {
                'status': 200,
                'data': quarterly_counts
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

    def get_yearly_data(self, query_filter, current_time):
        try:
            database_object = self.mongo["Buildings"]
            building = query_filter["building"]
            collection = database_object[building]
            yearly_counts = []
            

            entry_offset = 17280
            time_offset = 1440
            

            endpoints = collection.find(query_filter).distinct('endpoint_id')

            endpoint_total = len(endpoints)
            
            for skip_index in range(0, 369):
                new_time_offset = time_offset * skip_index
                segmented_counts = []
                skip_count = skip_index * entry_offset
                yearly_room_cursor = collection.find(query_filter).skip( skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

                for item in yearly_room_cursor:
                    segmented_counts.append(item['count'])
                    
                yearly_counts.append(self.__average_counts_by_time(segmented_counts, current_time, new_time_offset, endpoint_total))

            json_response = {
                'status': 200,
                'data': yearly_counts
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

    def __average_counts_by_time(self, segmented_counts, current_time, time_offset, endpoint_total):
        total_count = 0

        if(segmented_counts is None):
            total_avg_count = 0
        else:
            for count in segmented_counts:
                total_count += count

            total_avg_count = math.floor(total_count / endpoint_total * len(segmented_counts) )

            json_time = current_time - timedelta(minutes = time_offset)

        count_json = {'timestamp': json_time, 'count' : total_avg_count}

        return count_json