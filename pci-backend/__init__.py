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

    @app.route('/')
    def hello():
        return 'Base URL endpoint has been hit!'

    return app

