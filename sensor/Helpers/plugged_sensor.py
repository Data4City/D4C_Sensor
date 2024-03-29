import importlib
import logging
from datetime import datetime


class PluggedSensor:
    def __init__(self, sensor_info, i2c):
        self.logger = logging.getLogger(__name__)

        try:
            module = importlib.import_module(sensor_info["module"])
            constructor = getattr(module, sensor_info["constructor"])
            self.__sensor__ = constructor(i2c)
            self.api_id = sensor_info["api_id"]
            self.type = "i2c"
            self.name = sensor_info["name"]
            self.model = sensor_info["model"]
            self.sensor_data = self.construct_sensor_measurements(sensor_info)  # List containing Sensor Data objects
        except ImportError:
            self.logger.error("Could not load {}".format(sensor_info["imports"]))

    def construct_sensor_measurements(self, sensor_info):
        data = []
        sensor_data = sensor_info.get("measurements", [])
        for unit_sensor in sensor_data:
            curr_lambda = lambda: getattr(self.__sensor__, unit_sensor["function"])
            sensor = SensorMeasurement(unit_sensor, curr_lambda, unit_sensor["api_id"])
            data.append(sensor)
        return data

    def update_sensors(self) -> bool:
        """Tries to update the sensors and if it's successful it returns a boolean if any measurement gets updated"""
        result = False
        for curr_sensor in self.sensor_data:
            if not curr_sensor.check_only_once:
                if (datetime.now() - curr_sensor.timestamp).total_seconds() >= curr_sensor.check_every:
                    # Check if the difference is big enough to merit a change
                    delta = abs(curr_sensor.last_value * curr_sensor.threshold)
                    current = round(curr_sensor.function(), 2)
                    if curr_sensor.last_value + delta > current or curr_sensor.last_value - delta < current:
                        curr_sensor.update()
                        result = True

        return result

    def pre_process_api_post(self):
        post_data = []
        for i, data in enumerate(self.sensor_data):
            if not data.enqueued:
                post_data.append(data.__post_data__)
                data.enqueued = True

        return post_data

    def __str__(self) -> str:
        return "{} {} {} \n{} ".format(self.name, self.type, self.model,
                                       ' '.join(str(sensor) for sensor in self.sensor_data))

    def __post_data__(self, sensor_idx:int) -> dict:
        return {"name": self.name, "model": self.model, "type": "i2c","values": self.sensor_data[int(sensor_idx)].__post_data__}


class SensorMeasurement:
    def __init__(self, unit_sensor, data_lambda, measurement_id):
        self.timestamp = datetime.now()
        self.check_only_once = True if unit_sensor["check_every"] == 0 else False
        self.check_every = unit_sensor["check_every"]
        self.threshold = unit_sensor["threshold"]
        self.symbol = unit_sensor["symbol"]  # SI unit that measures the value given
        self.measurement_id = measurement_id
        self.last_value = data_lambda()
        self.function = data_lambda
        self.enqueued = False

    def update(self):
        # Update and add to queue if still not in server
        if not self.enqueued:
            self.last_value = round(self.function(), 2)
            self.timestamp = datetime.now()
            self.enqueued = False

    def __str__(self):
        return "{} {} last updated at: {}\n".format(self.last_value, self.symbol, self.timestamp)

    @property
    def __post_data__(self):
        return {"timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'), "value": self.last_value,
                "measurement_id": self.measurement_id}
