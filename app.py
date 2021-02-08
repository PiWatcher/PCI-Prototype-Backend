import logging
import os
import config

from api import api
from flask import Flask
from flask_cors import CORS

# setting up logging basic config
logging.basicConfig(level=logging.DEBUG,
                    format=f'[%(asctime)s]: {os.getpid()} %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

# setup logger
logger = logging.getLogger()

def create_app():
    logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)

    logger.info(f'Loading Flask application configurations')
    app.config.from_object('config')

    logger.info(f'Initializing cross-origin resource sharing')
    CORS(app)

    logger.info(f'Initializing PCI-REST API backend')
    api.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)