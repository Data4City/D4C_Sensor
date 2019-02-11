import unittest
from falcon import testing
from routes import get_app

class MyTestCase(testing.TestCase):
    def setUp(self):
        super(MyTestCase, self).setUp()
        self.app = get_app()


class TestMyApp(MyTestCase):
    def test_get_message(self):
        result = self.simulate_post('/kit')
        self.assertEqual("WAt", result.text)


if __name__ == '__main__':
    unittest.main()