import os

from flask import Flask

def create_app(test_config=None):
    # create and configure application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config passed in
        app.config.from_mapping(test_config)

    # check if the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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

    return app

