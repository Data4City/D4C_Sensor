import unittest
from falcon import testing
from routes import get_app



class MyTestCase(testing.TestCase):
    def setUp(self):
        super(MyTestCase, self).setUp()
        self.app = get_app()


class TestKitResource(MyTestCase):
    def test_create_kit(self):
        create_body = {'serial': "E00R000050600000"}
        assert_dict = {'serial': "E00R000050600000",
         'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'sensors_used': []
         }
        result = self.simulate_post('/kit', json = create_body)
        self.assertEqual(assert_dict, result.json)

        # Post again to test if it doesnt' create a second one .
        result = self.simulate_post('/kit')
        self.assertEqual({"error": "Box already exists"}, result.json)



#Ignoring datetime 
import datetime
constant_now = datetime.datetime(2009,8,7,6,5,4)
old_datetime_class = datetime.datetime
class new_datetime(datetime.datetime):
    @staticmethod
    def now():
        return constant_now

datetime.datetime = new_datetime

if __name__ == '__main__':
    unittest.main()