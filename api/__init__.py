from api.resources import *
from flask_restful import Api
from pymongo import MongoClient
from api.models.RoleModel import Role
from api.models.AccountModel import Account

import config

# instantiate Api with config API prefix
api = Api(prefix=config.API_PREFIX)

# instantiate mongo instance
mongo = MongoClient(config.MONGODB_URI)

# attempt to grab admin and public roles
admin_role = mongo["Users"]["roles"].find_one({
    'role_name': "admin"
})

public_role = mongo["Users"]["roles"].find_one({
    'role_name': "public"
})

# check if default admin is created
default_admin = mongo["Users"]["users"].find_one({
    'email': 'iotadmin@nau.edu'
})

# check if default roles is None
if admin_role is None:
    mongo["Users"]["roles"].insert_one(
        Role("admin", True, True).to_json()
    )

if public_role is None:
    mongo["Users"]["roles"].insert_one(
        Role("public", False, False).to_json()
    )

# create if there isn't
if default_admin is None:
    mongo["Users"]["users"].insert_one(
        Account('iotadmin@nau.edu', 'password', 'Administrator', 'admin').hash_password().to_json()
    )

# Add resource to api
api.add_resource(ApiBaseResource, '')

# authentication resources
api.add_resource(ApiAuthSignup, '/auth/signup')
api.add_resource(ApiAuthSignin, '/auth/signin')
api.add_resource(ApiAuthToken, '/auth/token')
api.add_resource(ApiAuthUsers, '/auth/users')
api.add_resource(ApiAuthUsersUpdate, '/auth/users/update')
api.add_resource(ApiAuthUsersUpdatePassword, '/auth/users/update/password')
api.add_resource(ApiAuthRoles, '/auth/roles')

# data resources
api.add_resource(ApiDataBuildingRooms, '/data/building/rooms')
api.add_resource(ApiDataBuildingRoomLive, '/data/building/room/live')
api.add_resource(ApiDataBuildingRoomDaily, '/data/building/room/daily')
api.add_resource(ApiDataBuildingRoomWeekly, '/data/building/room/weekly')
api.add_resource(ApiDataBuildingRoomMonthly, '/data/building/room/monthly')
api.add_resource(ApiDataBuildingRoomQuarterly, '/data/building/room/quarterly')
api.add_resource(ApiDataBuildingRoomYearly, '/data/building/room/yearly')
api.add_resource(ApiDataBuildings, '/data/buildings')
api.add_resource(ApiDataIotUpdate, '/data/iot/update')

# mock resources
api.add_resource(ApiMockResource, '/mock/update')
