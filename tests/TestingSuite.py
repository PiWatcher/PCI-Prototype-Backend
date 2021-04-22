import unittest
import json

# import parallel modules
import sys
sys.path.append('../')

from app import app
from api import mongo

class BaseTestingSuite(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.database = mongo
    
    def tearDown(self):
        # Delete databases after the test is complete
        
        databases = self.database.list_database_names()

        databases.remove("admin")
        databases.remove("config")
        databases.remove("local")

        for database in databases:
            print(database)
            self.database.drop_database(database)