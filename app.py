import logging
import os
import config

from api import api
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

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

    app.config['SECRET_KEY'] = os.urandom(24)

    logger.info(f'Loading Flask application configurations')
    app.config.from_object('config')

    logger.info(f'Initializing cross-origin resource sharing')
    CORS(app)

    logger.info(f'Initializing JWT manager')
    jwt = JWTManager(app)

    logger.info(f'Initializing PCI-REST API backend')
    api.init_app(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host=config.BASE_URL, port=config.PORT)