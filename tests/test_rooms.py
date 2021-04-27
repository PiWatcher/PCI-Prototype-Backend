import json


from api.services.MongoManagerService import MongoManagerService as mms
from tests.TestingSuite import BaseTestingSuite

class TestRoomsResource(BaseTestingSuite):
    def setUp(self):
        print('Testing Rooms resounrces...')
        super().setUp()

        # create mock data
        mms().mock_data_entry("Siccs", 100)
        mms().mock_data_entry("Engineering", 100)

    def test_successful_room_counts_by_building(self):
        response = self.app.get('/api/data/building/rooms',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'building_name': 'Siccs'
                                })

        self.assertEqual('Room 101', response.json['data'][0]['_id'])
        self.assertEqual(100, len(response.json['data'][0]['room_capacity']))
        self.assertEqual(200, response.status_code)
    
    def test_bad_schema_room_counts_by_building(self):
        response = self.app.get('/api/data/building/rooms',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'not_a_valid_key': 'random'
                                })

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)



    