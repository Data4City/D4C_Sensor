import models
import unittest

from falcon import testing
from routes import get_app


class MyTestCase(testing.TestCase):
    def setUp(self):
        super(MyTestCase, self).setUp()
        self.app = get_app()


class TestKitResource(MyTestCase):
    @classmethod
    def setUpClass(cls):
        models.__reset_db__()

    def test_a_create_kit(self):
        create_body = {'serial': "E00R000050600000"}
        assert_dict = {'serial': "E00R000050600000", 'id': 1,'sensors_used': []}
        result = self.simulate_post('/kit', json = create_body)
        result_jay= result.json
        print(result_jay)
        result_jay.pop('created_at')
        self.assertEqual(assert_dict, result_jay)

        # Post again to test if it doesnt' create a second one .
        result = self.simulate_post('/kit', json = create_body)
        self.assertEqual({'error': "Box already exists"}, result.json)

    def test_b_get_kit(self):


        result = self.simulate_get("/kit", json={'id': 1})
        self.assertEqual({'error': "Box with id 2 doesn't exist"}, result.json)


        # Error because no response
        result = self.simulate_get("/kit")
        self.assertEqual({'error': "Bad Request"}, result.json)

        # Error because id that doesn't exist
        result = self.simulate_get("/kit", json={'id': 2})
        self.assertEqual({'error': "Box with id 2 doesn't exist"}, result.json)


if __name__ == '__main__':
    unittest.main()
