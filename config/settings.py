class BaseConfig():
    API_PREFIX = "/api"
    BASE_URL = "0.0.0.0"
    PORT = 5000
    TESTING = False
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    FLASK_ENV = "development"
    DEBUG = True
    MONGO_USER = ""
    MONGO_PASS = ""
    MONGO_HOSTNAME = "mongodb"
    MONGO_PORT = "27017"
    MONGODB_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOSTNAME}:{MONGO_PORT}/"

class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"
    MONGO_USER = ""
    MONGO_PASS = ""
    MONGODB_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.vdjw7.mongodb.net/"

class TestingConfiguration(BaseConfig):
    FLASK_ENV = "development"
    TESTING = True
    DEBUG = True