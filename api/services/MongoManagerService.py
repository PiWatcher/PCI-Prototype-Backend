import json
import math
import random

from flask import Response
from bson import json_util
from datetime import timedelta, datetime

from api.services.BaseService import BaseService
from api.models.EntryModel import Entry
from api.errors.errors import *

class MongoManagerService(BaseService):

    def collect_all_buildings(self):
        '''
        Collects all buildings names from the database

        @returns a response object
        '''

        try:
            buildings = super().get_database("Buildings").list_collection_names()

            # construct successful response
            return super().construct_response({
                'status': 200,
                'data': buildings
            })

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def collect_counts_of_buildings(self, building):
        '''
        Collects the most recent count from all the rooms in a buildings

        @raises SchemaValidationError if it is missing a required key

        @returns a response object
        '''

        try:
            rooms_and_counts_list = []
            rooms_and_counts = {}
            total_count = 0

            if building is None:
                raise SchemaValidationError

            rooms_and_counts_cursor = super().get_database("Buildings")[building].aggregate(
                [{
                    "$group": {
                        "_id": "$endpoint",
                        "room_capacity": {
                            "$push": "$room_capacity"
                        },
                        "current_count": {
                            "$last": "$count"
                            }
                        }
                }])

            for item in rooms_and_counts_cursor:
                rooms_and_counts[item["_id"]] = item["current_count"]
                rooms_and_counts_list.append(item)

            for room in rooms_and_counts:
                total_count += rooms_and_counts[room]

            return super().construct_response({
                'status': 200,
                'data': rooms_and_counts_list
            })

        # Schema Validation Error
        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def insert_entry_by_room(self, data):
        '''
        Inserts an entry into the database

        @raises SchemaValidationError if missing required fields

        @returns a response object
        '''

        try:
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

            timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')

            # create new entry
            new_entry = Entry(timestamp_obj,
                              building,
                              building_id,
                              count,
                              endpoint,
                              endpoint_id,
                              room_capacity).to_json()

            # attempt to insert entry into database
            super().get_database("Buildings")[building].insert_one(new_entry)

            check_entry = super().get_database("Buildings")[building].find_one(new_entry, {'_id': 0})

            if check_entry is None:
                raise FailedEntryCreationError

            return super().construct_response({
                'status': 200,
                'timestamp': timestamp,
                'message': f"New entry was added successfully {check_entry['count']}"
            })

        # Schema Validation Error
        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        # Failed Entry Creationg Error
        except FailedEntryCreationError:
            return super().construct_response(errors["FailedEntryCreationError"])

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'

            return super().construct_response(error_message)

    def mock_data_entry(self, building, iterations=10):
        '''
        A helper/debugger function for adding mock entries into the database

        @param building where to insert data entry into
        @param iterations the number of times to mock data

        @returns a response object
        '''

        for iteration in range(0, iterations):
            response = self.insert_entry_by_room(
                self.__prepare_mock_data(building))

        json_response = {
            'status': 200,
            'message': f'{iterations} entries of mock data was inserted into {building.capitalize()}'
        }

        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])

    def __prepare_mock_data(self, building):
        '''
        A private helper function for preparing mock data

        @param building where to mock data too
        @param iterations the number of iterations to mock

        @returns a json containing mocked data
        '''
        
        data = {}
        random_room = random.randint(100, 150)
        random_endpoint_id = random.randint(1, 4)
        random_count = random.randint(1, 50)

        data['timestamp'] = str(datetime.now())
        data['building'] = building.capitalize()
        data['building_id'] = 1
        data['count'] = random_count
        data['endpoint'] = f'Room 101'
        data['endpoint_id'] = f'EPID_1'
        data['room_capacity'] = 50

        return data

    def __data_segmenter(self, query_filter, upper_limit, time_offset, num_of_endpoints, entry_offset=None, is_live=False):
        '''
        Segments the data by the different date ranges to give you an average over time

        @param query_filter query filter that is used to filter through database data
        @param upper_limits the max number of entries that will be returned
        @param time_offset time to offset by in minutes
        @param num_of_endpoints the number of unique endpoints in the room
        @param entry_offset the number of entries to offset by
        @param is_live boolean flag to check for live data querying

        @returns a list of segmented data
        '''

        # constants
        DECREASING = -1
        BEGINNING = 0
        
        segmented_data = []
        
        # iterate through and segment, average, then append data
        for skip_index in range(0, upper_limit):
            # calculate new time interval
            new_time_offset = time_offset * skip_index

            room_entries = []

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
            room_cursor = super().get_database("Buildings")[query_filter["building"]].find(
                query_filter, {'count': 1}).sort('_id', DECREASING).skip(skip_counts).limit(limited_entries)

            # add all entries in the room
            for entry in room_cursor:
                room_entries.append(entry['count'])

            # average entries
            averaged_entries = self.__average_counts_by_time(
                room_entries, query_filter["timestamp"]["$lte"], new_time_offset, num_of_endpoints)

            # append entries to data
            segmented_data.insert(BEGINNING, averaged_entries)

        # return averaged segmented data
        return segmented_data
        
    def get_live_data(self, building, room):
        '''
        Grabs segmented data for the past hour

        @raises SchemaValidationError if missing required keys

        @param building the building to get live data for
        @param room the room to get live data for

        @returns a response object
        '''

        try:
            # validate schema
            if building is None:
                raise SchemaValidationError
            if room is None:
                raise SchemaValidationError

            # declare/initialize variables

            # 1/2 w/ 120 == 120ms
            # 1/4 w/ 240 == 8 seconds
            # 1/12 w/ 740 == 1 minute 8 seconds
            time_offset = 1/2
            number_of_entries = 240

            # construct time interval
            current_time = datetime.now()
            interval = current_time - timedelta(hours=2)

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
            endpoint_total = len(super().get_database("Buildings")[building].distinct('endpoint_id', query_filter))

            # grab averaged counts
            live_counts = self.__data_segmenter(query_filter,
                                                     number_of_entries,
                                                     time_offset,
                                                     endpoint_total,
                                                     is_live=True)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': live_counts
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def get_daily_data(self, building, room):
        '''
        Grabs segmented data for the past day

        @raises SchemaValidationError if missing required keys

        @param building the building to get daily data for
        @param room the room to get daily data for

        @returns a response object
        '''

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
            endpoint_total = len(super().get_database("Buildings")[building].distinct('endpoint_id', query_filter))

            # grab averaged counts
            daily_counts = self.__data_segmenter(query_filter,
                                                 number_of_entries,
                                                 time_offset,
                                                 endpoint_total,
                                                 entry_offset)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': daily_counts
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def get_weekly_data(self, building, room):
        '''
        Grabs segmented data for the past week

        @raises SchemaValidationError if missing required keys

        @param building the building to get weekly data for
        @param room the room to get weekly data for

        @returns a response object
        '''

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
            endpoint_total = len(super().get_database("Buildings")[building].distinct('endpoint_id', query_filter))

            # grab averaged counts
            weekly_counts = self.__data_segmenter(query_filter,
                                                  number_of_entries,
                                                  time_offset,
                                                  endpoint_total,
                                                  entry_offset)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': weekly_counts
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def get_monthly_data(self, building, room):
        '''
        Grabs segmented data for the past week

        @raises SchemaValidationError if missing required keys

        @param building the building to get weekly data for
        @param room the room to get weekly data for

        @returns a response object
        '''

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
            endpoint_total = len(super().get_database("Buildings")[building].distinct('endpoint_id', query_filter))

            # grab averaged counts
            monthly_counts = self.__data_segmenter(query_filter,
                                                   number_of_entries,
                                                   time_offset,
                                                   endpoint_total,
                                                   entry_offset)
            
            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': monthly_counts 
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def get_quarterly_data(self, building, room):
        '''
        Grabs segmented data for the past quarter

        @raises SchemaValidationError if missing required keys

        @param building the building to get quarter data for
        @param room the room to get quarter data for

        @returns a response object
        '''

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
            endpoint_total = len(super().get_database("Buildings")[building].distinct('endpoint_id', query_filter))

            # grab averaged counts
            quarterly_counts = self.__data_segmenter(query_filter,
                                                     number_of_entries,
                                                     time_offset,
                                                     endpoint_total,
                                                     entry_offset)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': quarterly_counts
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)
        
        
    def get_yearly_data(self, building, room):
        '''
        Grabs segmented data for the past year

        @raises SchemaValidationError if missing required keys

        @param building the building to get year data for
        @param room the room to get year data for

        @returns a response object
        '''

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
            endpoint_total = len(super().get_database("Buildings")[building].distinct('endpoint_id', query_filter))

            # grab averaged counts
            yearly_counts = self.__data_segmenter(query_filter,
                                                  number_of_entries,
                                                  time_offset,
                                                  endpoint_total,
                                                  entry_offset)

            # construct successful response with data
            return super().construct_response({
                'status': 200,
                'data': yearly_counts
            })

        except SchemaValidationError:
            return super().construct_response(errors["SchemaValidationError"])

        except (InternalServerError, Exception) as error:
            error_message = errors["InternalServerError"]
            error_message["error"] = f'{error}'
            return super().construct_response(error_message)

    def __average_counts_by_time(self, segmented_counts, current_time, time_offset, endpoint_total):
        '''
        Averages all the counts in the list into one average count

        @returns a single json containing the averaged count in that date range
        '''

        total_count = 0
        json_time = current_time
        json_time = current_time - timedelta(minutes=time_offset)

        if(len(segmented_counts) == 0):
            total_avg_count = 0
        else:
            for count in segmented_counts:
                total_count += count

            total_avg_count = math.ceil(total_count / len(segmented_counts))

        count_json = {'timestamp': json_time,
                      'count': total_avg_count}

        return count_json
