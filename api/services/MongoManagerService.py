import json
import math
import random

from flask import Response
from bson import json_util
from datetime import timedelta, datetime

from api.services.BaseService import BaseService
from api.models.EntryModel import EntryModel
from api.errors.errors import *

class MongoManagerService(BaseService):

    def collect_all_buildings(self):
        try:
            # database_object = self.mongo["Buildings"]
            buildings = super().get_database("Buildings").list_collection_names()

            # construct successful response
            return super().construct_response({
                'status': 200,
                'data': buildings
            })

        # Internal Server Error
        except (InternalServerError, Exception):
            return super().construct_response(errors["InternalServerError"])

    def collect_counts_of_buildings(self, query_filter={}):
        try:
            # database_object = self.mongo["Buildings"]
            building_name = query_filter.get("building_name", None)
            # collection = database_object[building]

            rooms_and_counts_list = []
            rooms_and_counts = {}
            total_count = 0

            if building_name is None:
                raise SchemaValidationError

            rooms_and_counts_cursor = super().get_database("Buildings")[building_name].aggregate(
                [{"$group": {"_id": "$endpoint", "current_count": {"$last": "$count"}}}])

            for item in rooms_and_counts_cursor:
                rooms_and_counts[item["_id"]] = item["current_count"]
                rooms_and_counts_list.append(item)

            # total_room = len(rooms_and_counts)

            for room in rooms_and_counts:
                total_count += rooms_and_counts[room]

            # json_response = {
            #     'status': 200,
            #     'data': rooms_and_counts_list
            # }

            return super().construct_response({
                'status': 200,
                'data': rooms_and_counts_list
            })

        # Schema Validation Error
        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        # Internal Server Error
        except (InternalServerError, Exception):
            return super().construct_response(errors["InternalServerError"])

    def insert_entry_by_room(self, data):
        try:
            # database_object = self.mongo["Buildings"]
            # collection_object = database_object[data["building"]]

            timestamp = data.get("timestamp", None)
            building = data.get("building", None)
            building_id = data.get("building_id", None)
            count = data.get("count", None)
            endpoint = data.get("endpoint", None)
            endpoint_id = data.get("endpoint_id", None)
            room_capacity = data.get("room_capacity", None)

            # validate schema
            if timestamp is None:
                raise SchemaValidationError
            
            if building is None or building_id is None:
                raise SchemaValidationError

            if count is None:
                raise SchemaValidationError

            if endpoint is None or endpoint_id is None:
                raise SchemaValidationError

            if room_capacity is None:
                raise SchemaValidationError

            # create new entry
            new_entry = EntryModel().to_json()

            # attempt to insert entry into database
            super().get_database["Buildings"][building].insert_one(new_entry)

            # check if entry is in database
            check_entry = super().get_database("Buildings")[building].find_one(new_entry)

            if check_entry is None:
                raise FailedEntryCreationError

            return super().construct_response({
                'status': 200,
                'timestamp': timestamp,
                'message': f"New entry was added successfully {new_entry}"
            })

            # json_response = {
            #     'status': 200,
            #     'timestamp': data['timestamp'],
            #     'message': f"[{data['building']} ({data['building_id']})] {data['endpoint']} ({data['endpoint_id']}) successfully added it's entry"
            # }

            # return Response(json.dumps(json_response, default=json_util.default),
            #                 mimetype='application/json',
            #                 status=200)

        # Schema Validation Error
        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        # Failed Entry Creationg Error
        except FailedEntryCreationError:
            return super().construct_response(errors["FailedEntryCreationError"])

        except (InternalServerError, Exception):
            return super().construct_response(errors["InternalServerError"])

    def mock_data_entry(self, building, iterations=10):

        for iteration in range(0, iterations):
            self.insert_entry_by_room(
                self.__prepare_mock_data(building, iterations))

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
        random_endpoint_id = random.randint(1, 4)
        random_count = random.randint(1, 50)

        data['timestamp'] = datetime.now()
        data['building'] = building.capitalize()
        data['building_id'] = 1
        data['count'] = random_count
        data['endpoint'] = f'Room 101'
        data['endpoint_id'] = f'EPID_1'
        data['room_capacity'] = 50

        return data

    def __data_segmenter(self, query_filter, upper_limit, time_offset, num_of_endpoints, entry_offset=None, is_live=False):
        # constants
        DECREASING = -1
        BEGINNING = 0
        
        segmented_data = []
        
        # iterate through and segment, average, then append data
        for skip_index in range(0, upper_limit):
            # calculate new time interval
            new_time_offset = time_offset * skip_index

            # check if we are querying live data
            if is_live:
                # skip by how many entries
                skip_counts = skip_index * num_of_endpoints

                # limit entries per query
                limited_entries = num_of_endpoints
            else:
                # skip by how many entries
                skip_counts = skip_index * entry_offset * num_of_endpoints

                # limit entries per query
                limited_entries = entry_offset * num_of_endpoints

            # grab cursor for rooms
            room_cursor = super().get_database("Buidlings")[query_filter["building"]].find(
                query_filter).sort('_id', DECREASING).skip(skip_counts).limit(limited_entries)

            # add all entries in the room
            room_entries = [item['count'] for item in room_cursor]

            # average entries
            averaged_entries = self.__average_counts_by_time(
                room_entries, query_filter["timestamp"]["$lte"], new_time_offset, num_of_endpoints)

            # append entries to data
            segmented_data.append(BEGINNING, averaged_entries)

        # return averaged segmented data
        return segmented_data
        
    def get_live_data(self, building, room):
        try:
            # validate schema
            if building is None:
                raise SchemaValidationError
            if room is None:
                raise SchemaValidationError

            # declare/initialize variables
            time_offset = 1/12
            total_count = 0
            number_of_entries = 717

            # construct time interval
            current_time = datetime.now()
            interval = current_time - timedelta(minutes=60)

            # construct query filter
            query_filter = {
                "timestamp": {
                    "$lte": current_time,
                    "$gte": interval
                },
                "building": building,
                "endpoint": room
            }

            # get the total number of endpoints in room
            endpoint_total = len(super().get_database("Buildings")[building].find(
                query_filter).distinct('endpoint_id'))

            # grab averaged counts
            live_counts = self.__data_segmenter(query_filter=query_filter, upper_limit=number_of_entries,
                time_offset=time_offset, num_of_endpoints=endpoint_total, is_live=True)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': live_counts
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except Exception as error:
            return super().construct_response(errors["InternalServerError"].add("error", f'{error}'))

        #     for skip_index in range(0, 717):
        #         new_time_offset = time_offset * skip_index
        #         segmented_counts = []
        #         live_room_counts_cursor = collection.find(query_filter).sort('_id', -1).skip(
        #             skip_index * endpoint_total).limit(endpoint_total)

        #         for item in live_room_counts_cursor:
        #             segmented_counts.append(item['count'])

        #         live_counts.insert(0, self.__average_counts_by_time(
        #             segmented_counts, current_time, new_time_offset, endpoint_total))

        #     json_response = {
        #         'status': 200,
        #         'data': live_counts
        #     }

        #     return Response(json.dumps(json_response, default=json_util.default),
        #                     mimetype='application/json',
        #                     status=200)

        # except Exception as error:
        #     json_response = {
        #         'status': 400,
        #         'error': f'{error}'
        #     }

        # return Response(json.dumps(json_response),
        #                 mimetype='application/json',
        #                 status=400)

    def get_daily_data(self, building, room):
        try:
            # Validate schema
            if building is None:
                raise SchemaValidationError
            if room is None:
                raise SchemaValidationError

            # declare/initialize
            entry_offset = 60
            time_offset = 5
            number_of_entries = 288

            current_time = datetime.now()
            interval = current_time - timedelta(minutes=1440)

            # construct query filter
            query_filter = {
                "timestamp": {
                    "$lte": current_time,
                    "$gte": interval
                },
                "building": building,
                "endpoint": room
            }

            # get the total number of endpoints in room
            endpoint_total = len(super().get_database("Buildings")[building].find(
                query_filter).distinct('endpoint_id'))

            # grab averaged counts
            daily_counts = self.__data_segmenter(query_filter=query_filter, upper_limit=number_of_entries,
                time_offset=time_offset, num_of_endpoints=endpoint_total, entry_offset=entry_offset)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': daily_counts
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except Exception as error:
            return super().construct_response(errors["InternalServerError"].add("error", f'{error}'))

        #     database_object = self.mongo["Buildings"]
        #     building = query_filter["building"]
        #     collection = database_object[building]
        #     daily_counts = []

        #     entry_offset = 60
        #     time_offset = 5

        #     endpoints = collection.find(query_filter).distinct('endpoint_id')

        #     endpoint_total = len(endpoints)

        #     for skip_index in range(0, 288):
        #         new_time_offset = time_offset * skip_index
        #         segmented_counts = []
        #         # skip_count = skip_index * entry_offset
        #         daily_room_cursor = collection.find(query_filter).sort('_id', -1).skip(
        #             skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

        #         for item in daily_room_cursor:
        #             segmented_counts.append(item['count'])

        #         daily_counts.insert(0, self.__average_counts_by_time(
        #             segmented_counts, current_time, new_time_offset, endpoint_total))

        #     json_response = {
        #         'status': 200,
        #         'data': daily_counts
        #     }

        #     return Response(json.dumps(json_response, default=json_util.default),
        #                     mimetype='application/json',
        #                     status=200)

        # except Exception as error:
        #     json_response = {
        #         'status': 400,
        #         'error': f'{error}'
        #     }

        # return Response(json.dumps(json_response),
        #                 mimetype='application/json',
        #                 status=400)

    def get_weekly_data(self, building, room):
        try:
            # Validate Schema
            if building is None:
                raise SchemaValidationError
            if room is None:
                raise SchemaValidationError

            entry_offset = 720
            time_offset = 60
            number_of_entries = 168

            current_time = datetime.now()
            interval = current_time - timedelta(minutes=10080)

            query_filter = {
                'timestamp': {
                    '$lte': current_time,
                    '$gte': interval
                },
                'building': building,
                'endpoint': room
            }

            # get the total number of endpoints in room
            endpoint_total = len(super().get_database("Buildings")[building].find(
                query_filter).distinct('endpoint_id'))

            # grab averaged counts
            weekly_counts = self.__data_segmenter(query_filter=query_filter, upper_limit=number_of_entries,
                time_offset=time_offset, num_of_endpoints=endpoint_total, entry_offset=entry_offset)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': weekly_counts
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except Exception as error:
            return super().construct_response(errors["InternalServerError"].add("error", f'{error}'))

        #     database_object = self.mongo["Buildings"]
        #     building = query_filter["building"]
        #     collection = database_object[building]
        #     weekly_counts = []

        #     entry_offset = 720
        #     time_offset = 60

        #     endpoints = collection.find(query_filter).distinct('endpoint_id')

        #     endpoint_total = len(endpoints)

        #     for skip_index in range(0, 168):
        #         new_time_offset = time_offset * skip_index
        #         segmented_counts = []
        #         skip_count = skip_index * entry_offset
        #         weekly_room_cursor = collection.find(query_filter).sort('_id', -1).skip(
        #             skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

        #         for item in weekly_room_cursor:
        #             segmented_counts.append(item['count'])

        #         weekly_counts.insert(0, self.__average_counts_by_time(
        #             segmented_counts, current_time, new_time_offset, endpoint_total))

        #     json_response = {
        #         'status': 200,
        #         'data': weekly_counts
        #     }

        #     return Response(json.dumps(json_response, default=json_util.default),
        #                     mimetype='application/json',
        #                     status=200)

        # return Response(json.dumps(json_response),
        #                 mimetype='application/json',
        #                 status=400)

    def get_monthly_data(self, building, room):
        try:
            # validate schema
            if building is None:
                raise SchemaValidationError
            if room is None:
                raise SchemaValidationError
            
            # declare/initialize
            entry_offset = 720
            time_offset = 60
            number_of_entries = 731

            current_time = datetime.now()
            interval = datetime.now() - timedelta(minutes=302400)

            query_filter = {
                'timestamp': {
                    '$lte': current_time,
                    '$gte': interval
                },
                'building': building,
                'endpoint': room
            }

            # get the total number of endpoints in room
            endpoint_total = len(super().get_database("Buildings")[building].find(
                query_filter).distinct('endpoint_id'))

            # grab averaged counts
            monthly_counts = self.__data_segmenter(query_filter=query_filter, upper_limit=number_of_entries,
                time_offset=time_offset, num_of_endpoints=endpoint_total, entry_offset=entry_offset)
            
        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except Exception as error:
            return super().construct_response(errors["InternalServerError"].add("error", f'{error}'))

        #     database_object = self.mongo["Buildings"]
        #     building = query_filter["building"]
        #     collection = database_object[building]
        #     monthly_counts = []

        #     entry_offset = 720
        #     time_offset = 60

        #     endpoints = collection.find(query_filter).distinct('endpoint_id')

        #     endpoint_total = len(endpoints)

        #     for skip_index in range(0, 731):
        #         new_time_offset = time_offset * skip_index
        #         segmented_counts = []
        #         skip_count = skip_index * entry_offset
        #         monthly_room_cursor = collection.find(query_filter).sort('_id', -1).skip(
        #             skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

        #         for item in monthly_room_cursor:
        #             segmented_counts.append(item['count'])

        #         monthly_counts.insert(0, self.__average_counts_by_time(
        #             segmented_counts, current_time, new_time_offset, endpoint_total))

        #     json_response = {
        #         'status': 200,
        #         'data': monthly_counts
        #     }

        #     return Response(json.dumps(json_response, default=json_util.default),
        #                     mimetype='application/json',
        #                     status=200)

        # except Exception as error:
        #     json_response = {
        #         'status': 400,
        #         'error': f'{error}'
        #     }

        # return Response(json.dumps(json_response),
        #                 mimetype='application/json',
        #                 status=400)

    def get_quarterly_data(self, building, room):
        try:
            if building is None:
                raise SchemaValidationError
            if room is None:
                raise SchemaValidationError

            entry_offset = 17280
            time_offset = 1440
            number_of_entries = 168

            current_time = datetime.now()
            interval = current_time - timedelta(minutes=907200)

            query_filter = {
                'timestamp': {
                    '$lte': current_time,
                    '$gte': interval
                },
                'building': building,
                'endpoint': room
            }

            # get the total number of endpoints in room
            endpoint_total = len(super().get_database("Buildings")[building].find(
                query_filter).distinct('endpoint_id'))

            # grab averaged counts
            quarterly_counts = self.__data_segmenter(query_filter=query_filter, upper_limit=number_of_entries,
                time_offset=time_offset, num_of_endpoints=endpoint_total, entry_offset=entry_offset)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': quarterly_counts
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except Exception as error:
            return super().construct_response(errors["InternalServerError"].add("error", f'{error}'))
        
        # try:
        #     database_object = self.mongo["Buildings"]
        #     building = query_filter["building"]
        #     collection = database_object[building]
        #     quarterly_counts = []

        #     entry_offset = 17280
        #     time_offset = 1440

        #     endpoints = collection.find(query_filter).distinct('endpoint_id')

        #     endpoint_total = len(endpoints)

        #     for skip_index in range(0, 92):
        #         new_time_offset = time_offset * skip_index
        #         segmented_counts = []
        #         skip_count = skip_index * entry_offset
        #         quarterly_room_cursor = collection.find(query_filter).sort('_id', -1).skip(
        #             skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

        #         for item in quarterly_room_cursor:
        #             segmented_counts.append(item['count'])

        #         quarterly_counts.insert(0, self.__average_counts_by_time(
        #             segmented_counts, current_time, new_time_offset, endpoint_total))

        #     json_response = {
        #         'status': 200,
        #         'data': quarterly_counts
        #     }

        #     return Response(json.dumps(json_response, default=json_util.default),
        #                     mimetype='application/json',
        #                     status=200)

        # except Exception as error:
        #     json_response = {
        #         'status': 400,
        #         'error': f'{error}'
        #     }

        # return Response(json.dumps(json_response),
        #                 mimetype='application/json',
        #                 status=400)

    def get_yearly_data(self, building, room):
        try:
            # Validate schema
            if building is None:
                raise SchemaValidationError
            if room is None:
                raise SchemaValidationError

            entry_offset = 17280
            time_offset = 1440
            number_of_entries = 368

            current_time = datetime.now()
            interval = current_time - timedelta(minutes=3628800)

            query_filter = {
                'timestamp': {
                    '$lte': current_time,
                    '$gte': interval
                },
                'building': building,
                'endpoint': room
            }

            # get the total number of endpoints in room
            endpoint_total = len(super().get_database("Buildings")[building].find(
                query_filter).distinct('endpoint_id'))

            # grab averaged counts
            yearly_counts = self.__data_segmenter(query_filter=query_filter, upper_limit=number_of_entries,
                time_offset=time_offset, num_of_endpoints=endpoint_total, entry_offset=entry_offset)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': yearly_counts
            })
        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])
        except Exception as error:
            return super().construct_response(errors["InternalServerError"].add("error", f'{error}'))

        # try:
        #     database_object = self.mongo["Buildings"]
        #     building = query_filter["building"]
        #     collection = database_object[building]
        #     yearly_counts = []

        #     entry_offset = 17280
        #     time_offset = 1440

        #     endpoints = collection.find(query_filter).distinct('endpoint_id')

        #     endpoint_total = len(endpoints)

        #     for skip_index in range(0, 368):
        #         new_time_offset = time_offset * skip_index
        #         segmented_counts = []
        #         skip_count = skip_index * entry_offset
        #         yearly_room_cursor = collection.find(query_filter).sort('_id', -1).skip(
        #             skip_index * entry_offset * endpoint_total).limit(entry_offset * endpoint_total)

        #         for item in yearly_room_cursor:
        #             segmented_counts.append(item['count'])

        #         yearly_counts.insert(0, self.__average_counts_by_time(
        #             segmented_counts, current_time, new_time_offset, endpoint_total))

        #     json_response = {
        #         'status': 200,
        #         'data': yearly_counts
        #     }

        #     return Response(json.dumps(json_response, default=json_util.default),
        #                     mimetype='application/json',
        #                     status=200)

        # except Exception as error:
        #     json_response = {
        #         'status': 400,
        #         'error': f'{error}'
        #     }

        # return Response(json.dumps(json_response),
        #                 mimetype='application/json',
        #                 status=400)

    def __average_counts_by_time(self, segmented_counts, current_time, time_offset, endpoint_total):
        total_count = 0
        json_time = current_time
        json_time = current_time - timedelta(minutes=time_offset)

        if(len(segmented_counts) == 0):
            total_avg_count = 0
        else:
            for count in segmented_counts:
                total_count += count

            total_avg_count = math.floor(total_count / len(segmented_counts))

        count_json = {'timestamp': json_time,
                      'count': total_avg_count}

        return count_json
