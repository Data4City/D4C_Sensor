import busio, board, asyncio, logging
from Helpers import plugged_sensor, requests_handler, microphone
from threading import Thread


class Raspy:
    def __init__(self,serial, sensor_list):
        self.logger = logging.getLogger(__name__)
        self.current_plugged_sensors = []
        self.serial_num = serial
        self.threads = {}
        self.initialize_sensors(sensor_list)
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.initialize_sensors(sensor_list)

    def initialize_sensors(self, sensor_list):
        for sensor in sensor_list["sensors"]:
            try:
                self.current_plugged_sensors.append()
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
                    if sensor.type == "i2c":
                        for i, data in enumerate(sensor.sensor_data):
                            if not data.enqueued:
                                requests_handler.post_sensor.delay(sensor.__post_data__(i))
                                data.enqueued = True
            await asyncio.sleep(10)

    def create_thread(self, name, function):
        self.threads[name] = Thread(target=function)

    def start_threads(self):
        self.create_thread("sense", self.start_sense_loop)
        # TODO check this
        for key, value in self.threads.items():
            value.start()

    def sensor_factory(self, sensor_info):
        try:
            if sensor_info["type"] == "i2c":
                self.current_plugged_sensors.append(plugged_sensor.PluggedSensor(sensor_info, self.i2c))
                self.logger.info("{} sensor initialized".format(sensor_info["model"]))
            if sensor_info["type"] == "mic":
                mic = microphone.MicrophoneSensor(sensor_info)
                self.create_thread("microphone", mic.start_sensing)
        except RuntimeError:
            self.logger.error("{} sensor not found, ignoring".format(sensor_info["model"]))
