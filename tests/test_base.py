from tests.TestingSuite import BaseTestingSuite

class BaseResourceTest(BaseTestingSuite):
    def test_successful_response(self):
        response = self.app.get('/api', headers={
            "Content-Type": "application/json"
        })

        # then
        self.assertEqual(200, response.status_code)
        self.assertEqual(str, type(response.json['message']))