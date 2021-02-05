from flask import jsonify
from flask_restful import Resource

class ApiBaseResource(Resource):
    def get(self):
        return jsonify({'status': 200, 'message': 'Api base resource has been hit'})