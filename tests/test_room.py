import json

from api.services.MongoManagerService import MongoManagerService as mms
from tests.TestingSuite import BaseTestingSuite

class TestRoomResources(BaseTestingSuite):

    def setUp(self):
        print("Testing Room resources...")
        super().setUp()

        mms().mock_data_entry('Siccs', 1000)

    def test_successful_live_data(self):
        response = self.app.get('/api/data/building/room/live',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'building_name': 'Siccs',
                                    'room': 'Room 101'
                                })
        
        # 120 is the number of points for live data
        self.assertEqual(120, len(response.json['data']))
        self.assertEqual(200, response.status_code)

    def test_bad_schema_live_data(self):
        response = self.app.get('/api/data/building/room/live',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'bad_key_here': 'badbadbad',
                                    'room': 'Room 101'
                                })

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_successful_daily_data(self):
        response = self.app.get('/api/data/building/room/daily',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'building_name': 'Siccs',
                                    'room': 'Room 101'
                                })

        # 288 is the number of points for daily data
        self.assertEqual(288, len(response.json['data']))
        self.assertEqual(200, response.status_code)

    def test_bad_schema_daily_data(self):
        response = self.app.get('/api/data/building/room/daily',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'bad_key_here': 'badbadbad',
                                    'room': 'Room 101'
                                })

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_successful_weekly_data(self):
        response = self.app.get('/api/data/building/room/weekly',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'building_name': 'Siccs',
                                    'room': 'Room 101'
                                })

        # 168 is the number of points for daily data
        self.assertEqual(168, len(response.json['data']))
        self.assertEqual(200, response.status_code)

    def test_bad_schema_weekly_data(self):
        response = self.app.get('/api/data/building/room/weekly',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'bad_key_here': 'badbadbad',
                                    'room': 'Room 101'
                                })

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_successful_monthly_data(self):
        response = self.app.get('/api/data/building/room/monthly',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'building_name': 'Siccs',
                                    'room': 'Room 101'
                                })

        # 731 is the number of points for daily data
        self.assertEqual(731, len(response.json['data']))
        self.assertEqual(200, response.status_code)

    def test_bad_schema_monthly_data(self):
        response = self.app.get('/api/data/building/room/monthly',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'bad_key_here': 'badbadbad',
                                    'room': 'Room 101'
                                })

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_successful_quarterly_data(self):
        response = self.app.get('/api/data/building/room/quarterly',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'building_name': 'Siccs',
                                    'room': 'Room 101'
                                })

        # 168 is the number of points for daily data
        self.assertEqual(168, len(response.json['data']))
        self.assertEqual(200, response.status_code)

    def test_bad_schema_quarterly_data(self):
        response = self.app.get('/api/data/building/room/quarterly',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'bad_key_here': 'badbadbad',
                                    'room': 'Room 101'
                                })

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_successful_yearly_data(self):
        response = self.app.get('/api/data/building/room/yearly',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'building_name': 'Siccs',
                                    'room': 'Room 101'
                                })

        # 368 is the number of points for daily data
        self.assertEqual(368, len(response.json['data']))
        self.assertEqual(200, response.status_code)

    def test_bad_schema_yearly_data(self):
        response = self.app.get('/api/data/building/room/yearly',
                                headers={
                                    'Content-Type': 'application/json'
                                },
                                query_string={
                                    'bad_key_here': 'badbadbad',
                                    'room': 'Room 101'
                                })

        self.assertEqual('Request is missing required fields.', response.json['message'])
        self.assertEqual(400, response.status_code)