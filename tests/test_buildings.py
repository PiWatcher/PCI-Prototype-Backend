import json

from api.services.MongoManagerService import MongoManagerService as mms
from tests.TestingSuite import BaseTestingSuite

class TestBuildingsResource(BaseTestingSuite):

    def setUp(self):
        print("Testing Buildings resources...")
        super().setUp()

        mms().mock_data_entry('Siccs', 100)


    def test_successfully_collecting_buildings(self):
        response = self.app.get('/api/data/buildings',
                                headers={
                                    'Content-Type': 'application/json'
                                })

        self.assertEqual('Siccs', response.json['data'][0])
        self.assertEqual(200, response.status_code)
        
