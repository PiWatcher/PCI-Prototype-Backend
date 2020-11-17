import os

from flask import Flask

# create and configure flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev'
)

# load instance configuration
app.config.from_pyfile('config.py', silent=True)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# import resources
from backend.resources import BaseResource