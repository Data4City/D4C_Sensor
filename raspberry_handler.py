import asyncio
import logging
from threading import Thread

from Helpers import microphone
from Helpers.general_helpers import find_occurence_in_list
from Helpers.plugged_sensor import PluggedSensor
from Helpers.requests_handler import RequestHandler


class Raspy:
    def __init__(self, serial, config=None):
        self.logger = logging.getLogger(__name__)
        self.current_plugged_sensors = []
        self.serial_num = serial
        self.threads = {}
        self.requests_handler = None
        self.i2c = None

        if config:
            self.init_config(config)

    def init_config(self, config):
        try:
            import board
            import busio

            self.requests_handler = RequestHandler(config["api"])
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.initialize_sensors(self.compare_sensors_with_api(config["sensors"]))
        except Exception as e:
            self.logger.error("Could not initialize config. Error {}".format(e))

    def compare_sensors_with_api(self, sensor_list):
        kit = self.requests_handler.get_kit(self.serial_num)
        if 'error' in kit:
            kit = self.requests_handler.post_kit(self.serial_num)
        api_sensors_used = kit.get("sensors_used", [])
        for sensor in sensor_list:
            sensor_from_api = find_occurence_in_list(api_sensors_used, lambda x: x.get("model", None) == sensor["model"])
            if not sensor_from_api:
                api_sensor_create_response = self.requests_handler.post_sensor(sensor)
                sensor["api_id"] = api_sensor_create_response["id"]
            else:
                sensor["api_id"] = sensor_from_api["id"]

            measurements_api = sensor_from_api.get("measurements", [])
            measurements_config = sensor.get("measurements", [])

            for measurement in measurements_config:
                resp_measurement = find_occurence_in_list(measurements_api, lambda x: x.get("name", None) == measurement["name"])

                if not resp_measurement:
                    api_response = self.requests_handler.post_measurement(measurement)
                    measurement["api_id"] = api_response["id"]
                else:
                    measurement["api_id"] = resp_measurement["id"]

            sensor["measurements"] = measurements_config
        return sensor_list

    def initialize_sensors(self, checked_sensor_list):
        try:
            for sensor in checked_sensor_list:
                self.current_plugged_sensors.append(self.sensor_factory(sensor))
        except RuntimeError:
            self.logger.error("{} sensor not found, ignoring".format(sensor["model"]))

    def start_sense_loop(self):
        sensor_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(sensor_loop)
        asyncio.ensure_future(self.sense())
        sensor_loop.run_forever()

    async def sense(self):
        while True:
            for sensor in self.current_plugged_sensors:
                if sensor.update_sensors():
                    sensor.post_to_api()
            await asyncio.sleep(10)

    def create_thread(self, name, function):
        self.threads[name] = Thread(target=function)

    def start_threads(self):
        self.create_thread("sense", self.start_sense_loop)
        # TODO check this
        for key, value in self.threads.items():
            value.start()

    def sensor_factory(self, sensor_info):
        if sensor_info["type"] == "i2c":
            sensor = PluggedSensor(sensor_info, self.i2c)
            self.logger.info("{} sensor initialized".format(sensor_info["model"]))
            return sensor
        if sensor_info["type"] == "mic":
            mic = microphone.MicrophoneSensor(sensor_info)
            self.create_thread("microphone", mic.start_sensing)
            return mic
