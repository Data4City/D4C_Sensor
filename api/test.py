from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from falcon import testing
from routes import get_app
from datetime import datetime
import unittest, models


class MyTestCase(testing.TestCase):
    def setUp(self):
        super(MyTestCase, self).setUp()
        self.app = get_app()

class TestKitResource(MyTestCase):
    def test_create_kit(self):
        create_body = {'serial': "E00R000050600000"}
        assert_dict = {'serial': "E00R000050600000", 'id': 1,'sensors_used': []}
        result = self.simulate_post('/kit', json = create_body)
        result_jay= result.json

        result_jay.pop('created_at')
        self.assertEqual(assert_dict, result_jay)

        # Post again to test if it doesnt' create a second one .
        result = self.simulate_post('/kit', json = create_body)
        self.assertEqual({'error': "Box already exists"}, result.json)

if __name__ == '__main__':
    models.__reset_db__()
    unittest.main()