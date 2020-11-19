import os

from flask import Flask
from flask_restful import Api

# create and configure flask app
app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev'
)

# load instance configuration
app.config.from_pyfile('config.py', silent=True)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# import resources
from backend.resources.ApiResource import *

api = Api(app)
api.add_resource(ApiBaseResource, '/api', '/api/')
api.add_resource(ApiBuidlingResource, '/api/<building>', '/api/<building>/all')
api.add_resource(ApiEndpointResource, '/api/<building>/<endpoint>', '/api/<building>/<endpoint>/')