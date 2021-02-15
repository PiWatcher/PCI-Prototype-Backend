from api.resources import *
from flask_restful import Api
from pymongo import MongoClient

import config

# instantiate Api with config API prefix
api = Api(prefix=config.API_PREFIX)

# instantiate mongo instance
mongo = MongoClient(config.MONGODB_URI)

# Add resource to api
api.add_resource(ApiBaseResource, '')
api.add_resource(ApiBuildingResource, '/building')
api.add_resource(ApiEntryResource, '/<building>')
api.add_resource(ApiUpdateResource, '/update')
api.add_resource(ApiSignupResource, '/signup')
api.add_resource(ApiSigninResource, '/signin')
