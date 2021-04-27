import unittest
import json

# import parallel modules
import sys
sys.path.append('../')

from app import app
from api import mongo
from api.models.AccountModel import Account
from api.models.RoleModel import Role

class BaseTestingSuite(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.database = mongo

        # attempt to grab admin and public roles
        admin_role = self.database["Users"]["roles"].find_one({
            'role_name': "admin"
        }, {"_id": 0})

        public_role = self.database["Users"]["roles"].find_one({
            'role_name': "public"
        }, {"_id": 0})

        # check if default roles is None
        if admin_role is None:
            self.database["Users"]["roles"].insert_one(
                Role("admin", True, True).to_json()
            )

        if public_role is None:
            self.database["Users"]["roles"].insert_one(
                Role("public", False, False).to_json()
            )

        # check if default admin is created
        default_admin = mongo["Users"]["users"].find_one({
            'email': 'iotadmin@nau.edu'
        }, {"_id": 0})

        # create if there isn't
        if default_admin is None:
            self.database["Users"]["users"].insert_one(
                Account('iotadmin@nau.edu', 'password', 'Administrator', 'admin').hash_password().to_json()
            )
    
    def tearDown(self):

        # Delete databases after the test is complete
        databases = self.database.list_database_names()

        databases.remove("admin")
        databases.remove("config")
        databases.remove("local")

        for database in databases:
            self.database.drop_database(database)