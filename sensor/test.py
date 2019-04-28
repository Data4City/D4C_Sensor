#!/usr/bin/env python
# -*- coding: utf-8 -*

import unittest
import mock

from sensor.raspberry_handler import Raspy


class RaspberryTestCase(unittest.TestCase):

    def setUp(self):
        self.raspy = Raspy("0000000000000000")

    def test_init_sensor_without_api_content(self):
        get_kit_return = {
            'id': 1,
            'sensors_used': [],
            'serial': 'E00R000050600000'
        }

        sensor_create = {
            'id': 1, 'model': 'TSL2591', 'name': 'High Dynamic Range Digital Light',
            'measurements': []
        }
        measurement_create = {'name': 'Lux', 'symbol': 'lx', "id": 1}


        self.raspy.requests_handler = mock.MagicMock()
        self.raspy.requests_handler.get_kit.return_value = {
            'error': "Kit with serial {} doesn't exist".format("0000000000000000")}
        self.raspy.requests_handler.post_kit.return_Value = get_kit_return
        self.raspy.requests_handler.post_sensor.return_value = sensor_create
        self.raspy.requests_handler.post_measurement.return_value = measurement_create
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

    def test_init_sensor(self):
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
        self.raspy.requests_handler.post_sensor.return_value = get_kit_return["sensors_used"][0]

        self.raspy.requests_handler.post_measurement.return_value = get_kit_return["sensors_used"][0]["measurements"][0]
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
