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
            self.initialize_sensors(config["sensors"])
        except Exception as e:
            self.logger.error("Could not initialize config. Error {}".format(e))

    def initialize_sensors(self, sensor_list):
        kit = self.requests_handler.get_kit_id(self.serial_num)
        sensors_used = kit["sensors_used"]
        for sensor in sensor_list["sensors"]:
            try:
                sensor_api = find_occurence_in_list(sensors_used, lambda x: x.get("model", None) == sensor["model"])
                if sensor_api is None:
                    sensor["api"] = self.requests_handler.get_sensor(sensor)
                else:
                    sensor["api"] = sensor_api

                measurements_api = sensor_api.get("measurements", [])
                measurements_config = sensor.get("data", [])
                updated_measurements = []

                for measurement in measurements_config:
                    resp_measurement = find_occurence_in_list(measurements_api,
                                                              lambda x: x.get("name", None) == measurement["name"])

                    if resp_measurement is None:
                        updated_measurements.append(self.requests_handler.get_measurement(measurement))
                    else:
                        updated_measurements.append(resp_measurement)

                sensor["measurements"] = updated_measurements
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
