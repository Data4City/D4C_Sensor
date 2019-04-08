import importlib, logging
from datetime import datetime


class PluggedSensor:
    def __init__(self, sensor, i2c):
        self.logger = logging.getLogger(__name__)

        try:
            module = importlib.import_module(sensor["module"])
            constructor = getattr(module, sensor["constructor"])
            self.__sensor__ = constructor(i2c)

            self.type = "i2c"
            self.name = sensor["name"]
            self.model = sensor["model"]
            self.sensor_data = self.construct_sensor_data(sensor["data"])  # List containing Sensor Data objects
        except ImportError:
            self.logger.error("Could not load {}".format(sensor["imports"]))

    def construct_sensor_data(self, sensor_data):
        data = []
        for unit_sensor in sensor_data:
            curr_lambda = getattr(self.__sensor__, unit_sensor["function"])
            sensor = SensorData(unit_sensor, curr_lambda)
            data.append(sensor)
        return data

    def update_sensors(self) -> bool:
        """Tries to update the sensors and if it's successful it returns a boolean if any sensor gets updated"""
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

    def post_to_api(self):
        #TODO Implement this
        for i, data in enumerate(self.sensor_data):
            if not data.enqueued:
                requests_handler.post_sensor.delay(sensor.__post_data__(i))
                data.enqueued = True

    def __str__(self) -> str:
        return "{} {} {} \n{} ".format(self.name, self.type, self.model,
                                       ' '.join(str(sensor) for sensor in self.sensor_data))

    def __post_data__(self, sensor_idx="None") -> dict:
        if type(sensor_idx) == str:
            return {"name": self.name, "model": self.model, "type": "i2c"}
        else:
            return {"name": self.name, "model": self.model, "type": "i2c",
                    "data": self.sensor_data[int(sensor_idx)].__post_data__()}


class SensorData:
    def __init__(self, unit_sensor, data_lambda):
        self.timestamp = datetime.now()
        self.check_only_once = True if unit_sensor["check_every"] == 0 else False
        self.check_every = unit_sensor["check_every"]
        self.threshold = unit_sensor["threshold"]
        self.units = unit_sensor["unit"]  # SI unit that measures the value given
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
        return "{} {} last updated at: {}\n".format(self.last_value, self.units, self.timestamp)

    def __post_data__(self):
        return {"timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'), "value": self.last_value,
                "units": self.units}
