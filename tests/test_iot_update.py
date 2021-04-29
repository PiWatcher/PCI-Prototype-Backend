import json
import datetime
from bson import json_util

from tests.TestingSuite import BaseTestingSuite

class TestIotUpdateResource(BaseTestingSuite):
    def setUp(self):
        print("Testing Iot Update resources...")
        super().setUp()

    def test_successful_iot_entry(self):
        new_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'building': "test building",
            'building_id': "test id",
            'count': 10,
            'endpoint': "test endpoint",
            'endpoint_id':"test endpoint id",
            'room_capacity': 50
        }

        response = self.app.post('/api/data/iot/update',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                data=json.dumps(new_entry,
                                                default=json_util.default))

        self.assertEqual(f'New entry was added successfully {new_entry["count"]}', response.json['message'])
        self.assertEqual(200, response.status_code)

    def test_bad_schema_error(self):
        new_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'building': "test building",
            # 'building_id': "test id",
            'count': 10,
            'endpoint': "test endpoint",
            'endpoint_id':"test endpoint id",
            'room_capacity': 50
        }

        response = self.app.post('/api/data/iot/update',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                data=json.dumps(new_entry,
                                                default=json_util.default))
        
        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)
                            