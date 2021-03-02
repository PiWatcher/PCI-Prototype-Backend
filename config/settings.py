import os

class BaseConfig():
    API_PREFIX = "/api"
    BASE_URL = "0.0.0.0"
    PORT = 5000
    TESTING = False
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    FLASK_ENV = "development"
    DEBUG = True
    MONGO_USER = os.environ["MONGO_USER"]
    MONGO_PASS = os.environ["MONGO_PASS"]
    MONGO_HOSTNAME = os.environ["MONGO_HOSTNAME"]
    MONGO_PORT = os.environ["MONGO_PORT"]
    MONGODB_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOSTNAME}:{MONGO_PORT}/"

class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"
    MONGO_USER = os.environ["MONGO_USER"]
    MONGO_PASS = os.environ["MONGO_PASS"]
    MONGO_HOSTNAME = os.environ["MONGO_HOSTNAME"]
    MONGO_PORT = os.environ["MONGO_PORT"]
    MONGODB_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOSTNAME}:{MONGO_PORT}/"

class TestingConfiguration(BaseConfig):
    FLASK_ENV = "development"
    TESTING = True
    DEBUG = True