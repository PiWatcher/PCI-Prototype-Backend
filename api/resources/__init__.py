from flask import jsonify, request
from flask_restful import Resource

# authentication resources
from api.resources.auth.signin import ApiAuthSignin
from api.resources.auth.signup import ApiAuthSignup
from api.resources.auth.signout import ApiAuthSignout

from api.resources.auth.verify.resetcode import ApiAuthVerifyResetCode

from api.resources.auth.users import ApiAuthUsers, ApiAuthUsersUpdate, ApiAuthUsersUpdatePassword

from api.resources.auth.roles import ApiAuthRoles

# data resources
from api.resources.data import ApiDataBuildings
from api.resources.data.building.rooms import ApiDataBuildingRooms

from api.resources.data.building.room import ApiDataBuildingRoomLive
from api.resources.data.building.room import ApiDataBuildingRoomDaily
from api.resources.data.building.room import ApiDataBuildingRoomWeekly
from api.resources.data.building.room import ApiDataBuildingRoomMonthly
from api.resources.data.building.room import ApiDataBuildingRoomQuarterly
from api.resources.data.building.room import ApiDataBuildingRoomYearly

from api.resources.data.iot.update import ApiDataIotUpdate

from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

class ApiBaseResource(Resource):
    def get(self):
        return jsonify({'status': 200, 'message': 'Api base resource has been hit'})

class ApiMockResource(Resource):
    def get(self):
        building = request.args.get('building', type=str)
        iterations = request.args.get('iterations', default=10, type=int)

        response = mms().mock_data_entry(building, iterations)
        return response
