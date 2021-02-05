from api.resources import *
from flask_restful import Api

import config

# instantiate Api with config API prefix
api = Api(prefix=config.API_PREFIX)

# Add resource to api
api.add_resource(ApiBaseResource, '')