import asyncio
import logging
from asyncio import coroutine
from threading import Thread

from Helpers.general_helpers import find_occurence_in_list
from Helpers.plugged_sensor import PluggedSensor
import Helpers.requests_handler as rh
import config


class Raspy(Thread):
    def __init__(self, serial):
        Thread.__init__(self, group=None, target=None, name="Raspberry")
        self.logger = logging.getLogger(__name__)
        self.current_plugged_sensors = []
        self.serial_num = serial
        self.threads = {}
        self.i2c = None

        if config:
            self.init_config()

    def run(self):
        loop = asyncio.new_event_loop()
        self.threads["sense"] = Thread(name="sense", target=self.start_sense_loop, args=(loop,))
        for key, value in self.threads.items():
            self.logger.info("Starting thread".format(value.name))
            value.start()

    def init_config(self):
        import board
        import busio

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.initialize_sensors(self.compare_sensors_with_api(config.sensors))

    def compare_sensors_with_api(self, sensor_list):
        kit = rh.get_kit(self.serial_num)
        if 'error' in kit:
            kit = rh.post_kit(self.serial_num)
        api_sensors_used = kit.get("sensors_used", [])
        for sensor in sensor_list:
            sensor_from_api = find_occurence_in_list(api_sensors_used,
                                                     lambda x: x.get("model", None) == sensor["model"])
            if not sensor_from_api:
                api_sensor_create_response = rh.post_sensor(sensor)
                sensor["api_id"] = api_sensor_create_response["id"]
            else:
                sensor["api_id"] = sensor_from_api["id"]

            measurements_api = sensor_from_api.get("measurements", [])
            measurements_config = sensor.get("measurements", [])

            for measurement in measurements_config:
                resp_measurement = find_occurence_in_list(measurements_api,
                                                          lambda x: x.get("name", None) == measurement["name"])

                if not resp_measurement:
                    api_response = rh.post_measurement(sensor["api_id"], measurement)
                    measurement["api_id"] = api_response["id"]
                else:
                    measurement["api_id"] = resp_measurement["id"]

            sensor["measurements"] = measurements_config
        return sensor_list

    def initialize_sensors(self, checked_sensor_list):
        name = ""
        for sensor in checked_sensor_list:
            try:
                name = sensor.get("name", "No Model")
                sensor_obj = self.sensor_factory(sensor)
                self.current_plugged_sensors.append(sensor_obj)
            except RuntimeError:
                self.logger.error("{} sensor not found, ignoring".format(name))

    def start_sense_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.sense())

    @coroutine
    def sense(self):
        print("Starting sense loop")
        self.logger.info("Starting sense loop")
        while True:
            for sensor in self.current_plugged_sensors:
                if sensor.update_sensors():
                    sensor.post_to_api()
            yield from asyncio.sleep(10)

    def _create_thread(self, name, function, *args):
        self.logger.info("Creating thread {}".format(name))
        self.threads[name] = Thread(name=name, target=function, args=args)

    def sensor_factory(self, sensor_info):
        if sensor_info["type"] == "i2c":
            sensor = PluggedSensor(sensor_info, self.i2c)
            self.logger.info("{} sensor initialized".format(sensor_info["model"]))
            return sensor
        if sensor_info["type"] == "mic":
            try:
                from Helpers.microphone import MicrophoneSensor

                mic = MicrophoneSensor(sensor_info)
                self._create_thread("microphone", mic.start_sensing)
                return mic
            except Exception:
                raise RuntimeError
