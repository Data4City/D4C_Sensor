import importlib, logging

class PluggedSensor():
    def __init__(self, sensor, i2c):
        try:
            importlib.import_module(sensor["module"])
            constructor = getattr(sensor["module"], sensor["constructor"])
            self.__sensor__ = constructor(i2c)
        except ImportError:
            logger = logging.getLogger(__name__)
            logger.error("Could not load {}".format(sensor["imports"]))

        self.name = sensor["name"]
        self.model = sensor["model"]
        self.values = get_sensor_lambdas(sensor["data"])

    def get_sensor_lambdas(data):
        for unit in data:
            %TODO CREATE THIS FUNCTION