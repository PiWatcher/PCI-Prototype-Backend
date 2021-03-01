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

# authentication resources
api.add_resource(ApiSignupResource, '/auth/signup')
api.add_resource(ApiSigninResource, '/auth/signin')

# data resources
api.add_resource(ApiBuildingResource, '/data/buildings')
api.add_resource(ApiEntryResource, '/data/building')
api.add_resource(ApiUpdateResource, '/data/update')

# mock resources
api.add_resource(ApiMockResource, '/mock/update')
