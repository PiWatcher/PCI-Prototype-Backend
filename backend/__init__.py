import os

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient
from backend.config import MONGO_USER, MONGO_PASS

# create and configure flask app
app = Flask(__name__.split('.')[0])

MONGO_DB_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.vdjw7.mongodb.net/"
mongo = MongoClient(MONGO_DB_URI)

# import resources
from backend.resources.ApiResource import *

api = Api(app)

api.add_resource(ApiBaseResource, '/api')
api.add_resource(ApiBuildingResource, '/api/<building>')
api.add_resource(ApiRoomResource, '/api/<building>/<room>')
api.add_resource(ApiUpdateResource, '/api/update')