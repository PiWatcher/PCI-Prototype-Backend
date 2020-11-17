from backend import app
from backend.services import MongoService, RandomDataService

@app.route('/api/', methods=['GET'])
def base_api():
    return 'Base URL endpoint has been hit!'

@app.route('/api/<string:building>/all', methods=['GET'])
def grab_all_endpoints_for_building(building):
    return f'Queried {building}'

@app.route('/api/<string:building>/<string:endpoint>', methods=['GET'])
def grab_specific_endpoint_in_building(building, endpoint):
    return f'Queried {building} for endpoint: {endpoint}'

@app.route('/api/update', methods=['POST'])
def add_entry_to_database():
    return f'Adding entry to database'
