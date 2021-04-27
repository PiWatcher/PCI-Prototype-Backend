import api
import json
import bcrypt
import logging

from flask import Response
from bson import json_util

class BaseService():

    def __init__(self):
        self.mongo = api.mongo
        self.logger = logging.getLogger()

    def construct_response(self, json_response):
        '''
        Construct a response object with the corresponding json that is passed in.

        @param json_response the json dictionary that is going to be returned in the
                             body of the response

        @returns a response object
        '''

        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])

    def get_database(self, database_name):
        '''
        Returns a mongodb connection to the corresponding database

        @param database_name the database that needs to be accessed

        @return mongo connection to the database
        '''

        return self.mongo[database_name]

    def get_logger(self):
        '''
        Returns a logger object, that is useful for debugging.

        @return returns a logger object
        '''

        return self.logger