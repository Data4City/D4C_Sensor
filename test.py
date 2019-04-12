#!/usr/bin/env python
# -*- coding: utf-8 -*

import unittest
import mock

from raspberry_handler import Raspy


class RaspberryTestCase(unittest.TestCase):

    def setUp(self):
        self.raspy = Raspy("0000000000000000")

    @mock.patch("Helpers.requests_handler.RequestHandler")
    def test_init_sensor(self, mock_request_handler):
        get_kit_return = {
            'id': 1,
            'sensors_used': [
                {
                    'id': 1, 'model': 'TSL2591', 'name': 'High Dynamic Range Digital Light',
                    'measurements': [{'name': 'Lux', 'symbol': 'lx', "id": 1}]
                }
            ],
            'serial': 'E00R000050600000'}
        self.raspy.requests_handler = mock.MagicMock()
        self.raspy.requests_handler.get_kit_id.return_value = get_kit_return
        self.raspy.requests_handler.get_sensor.return_value = get_kit_return["sensors_used"]
        self.raspy.requests_handler.get_measurement.return_value = get_kit_return["sensors_used"][0]["measurements"]
        sensor_list = [
                {
                    "name": "High Dynamic Range Digital Light",
                    "model": "TSL2591",
                    "module": "adafruit_tsl2591",
                    "constructor": "TSL2591",
                    "type": "i2c",
                    "measurements": [
                        {
                            "check_every": 10,
                            "name": "Lux",
                            "symbol": "lx",
                            "function": "lux",
                            "threshold": 0.05
                        }
                    ]
                }
            ]
        assert_list = [{
            'name': 'High Dynamic Range Digital Light',
            'model': 'TSL2591', 'module': 'adafruit_tsl2591',
            'constructor': 'TSL2591',
            'type': 'i2c',
            'measurements': [
                {
                    'check_every': 10, 'name': 'Lux',
                    'symbol': 'lx', 'function': 'lux', 'threshold': 0.05,
                    'api_id': 1
                }
            ],
            'api_id': 1}
        ]
        self.raspy.init_config({})
        checked_sensor_list = self.raspy.compare_sensors_with_api(sensor_list)
        self.assertEqual(checked_sensor_list, assert_list)
