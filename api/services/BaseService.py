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
        return Response(json.dumps(json_response, default=json_util.default),
                        mimetype='application/json',
                        status=json_response['status'])

    def get_database(self, database_name):
        return self.mongo[database_name]

    def get_logger(self):
        return self.logger