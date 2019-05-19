import asyncio
import logging
from asyncio import coroutine
from threading import Thread

from Helpers import general_helpers as gh
from Helpers.plugged_sensor import PluggedSensor
import Helpers.requests_handler as rh
import config


class Raspy():
    def __init__(self, serial):
        self.logger = logging.getLogger(__name__)
        self.current_plugged_sensors = []
        self.threads = {}
        self.i2c = None
        self.kit_id = None
        if config:
            kit = rh.post_kit(serial)
            self.kit_id = kit.get("id", None)
            if not self.kit_id:
                self.logger.error("Error getting kit id")
            self.init_config()

    def init_config(self):
        import board
        import busio

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.initialize_sensors(self.compare_sensors_with_api(config.sensors))

    def initialize_sensors(self, checked_sensor_list):
        name = ""
        for sensor in checked_sensor_list:
            try:
                name = sensor.get("name", "No Model")
                sensor_obj = self.sensor_factory(sensor)
                if sensor_obj:
                    self.current_plugged_sensors.append(sensor_obj)
            except RuntimeError:
                self.logger.error("{} sensor not found, ignoring".format(name))

    def run(self):
        loop = asyncio.new_event_loop()
        self.threads["sense"] = Thread(name="sense", target=self.start_sense_loop, args=(loop,))
        for key, value in self.threads.items():
            self.logger.info("Starting thread".format(value.name))
            value.start()

    def start_sense_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.sense())

    def compare_sensors_with_api(self, sensor_list):
        kit = rh.get_kit(self.kit_id)

        api_sensors_used = kit.get("sensors_used", [])
        for sensor in sensor_list:
            sensor_from_api = gh.find_occurence_in_list(api_sensors_used,
                                                        lambda x: x.get("model", None) == sensor["model"])
            if not sensor_from_api:
                api_sensor_create_response = rh.post_sensor(name=sensor["name"], model=sensor["model"])
                sensor["api_id"] = api_sensor_create_response["id"]
            else:
                sensor["api_id"] = sensor_from_api["id"]

            measurements_api = sensor_from_api.get("measurements", [])
            measurements_config = sensor.get("measurements", [])

            for measurement in measurements_config:
                resp_measurement = gh.find_occurence_in_list(measurements_api,
                                                             lambda x: x.get("name", None) == measurement["name"])

                if not resp_measurement:
                    api_response = rh.post_measurement(sensor_id=sensor["api_id"], symbol=measurement['symbol'],
                                                       name=measurement['name'])
                    measurement["api_id"] = api_response["id"]
                else:
                    measurement["api_id"] = resp_measurement["id"]

            sensor["measurements"] = measurements_config
        return sensor_list

    @coroutine
    def sense(self):
        print("Starting sense loop")
        self.logger.info("Starting sense loop")
        while True:
            for sensor in self.current_plugged_sensors:
                if sensor.update_sensors():
                    to_post = sensor.pre_process_api_post()
                    if to_post:
                        for element in to_post:
                            print("Calling post event with data {}".format(str(element)))
                            rh.post_value.delay(config.api["base_url"], self.kit_id, element["measurement_id"],
                                                element["last_value"], element["timestamp"])
            yield from asyncio.sleep(10)

    def sensor_factory(self, sensor_info):
        if sensor_info["type"] == "i2c":
            sensor = PluggedSensor(sensor_info, self.i2c)
            self.logger.info("{} sensor initialized".format(sensor_info["model"]))
            return sensor
        # if sensor_info["type"] == "mic":
        #     try:
        #         from sensor.Helpers.microphone import MicrophoneSensor
        #
        #         mic = MicrophoneSensor(sensor_info)
        #         self.threads["Microphone"] = Thread(name="Microphone", target=mic.start_sensing())
        #
        #         return mic
        #     except Exception:
        #         raise RuntimeError
