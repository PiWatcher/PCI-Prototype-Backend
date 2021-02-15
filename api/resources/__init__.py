from flask import jsonify, request
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from api.services.MongoManagerService import MongoManagerService as mms
from api.services.LoginAuthenticationService import LoginAuthenticationService as las

auth = HTTPBasicAuth()

# temporary user data
USER_DATA = {
    "admin": "admin"
}

@auth.verify_password
def verify(username, password):
    if not(username and password):
        return False
    
    return USER_DATA.get(username) == password

class ApiBaseResource(Resource):
    @auth.login_required
    def get(self):
        return jsonify({'status': 200, 'message': 'Api base resource has been hit'})

class ApiBuildingResource(Resource):
    @auth.login_required
    def get(self):
        response = mms().collect_all_buildings()
        return response

class ApiEntryResource(Resource):
    @auth.login_required
    def get(self, building):
        response = mms().collect_all_entries_by_building(building)
        return response

class ApiUpdateResource(Resource):
    @auth.login_required
    def post(self):
        response = mms().insert_entry_by_room(request.json)
        return response

class ApiSignupResource(Resource):
    def post(self):
        return las().handle_signup(request.json) 

class ApiLoginResource(Resource):
    def post(self):
        return las().handle_signin(request.json)