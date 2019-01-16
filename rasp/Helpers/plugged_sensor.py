import importlib, logging
from datetime import datetime


class PluggedSensor():
    def __init__(self, sensor,i2c):
        try:
            module = importlib.import_module(sensor["module"])
            constructor = getattr(module, sensor["constructor"])
            self.__sensor__ = constructor(i2c)
        except ImportError:
            logger = logging.getLogger(__name__)
            logger.error("Could not load {}".format(sensor["imports"]))

        self.name = sensor["name"]
        self.model = sensor["model"]
        self.sensor_data = self.get_sensor_lambdas(sensor["data"])

    
    def get_sensor_lambdas(self, data):
        functions = []
        for unit in data:
            currLambda = lambda: getattr(self.__sensor__, unit["function"])
            functions.append(
                {
                'lambda': currLambda,
                'data': SensorData(once = unit["once"],
                unit = unit["unit"], 
                last_value=currLambda()),
            })
        return functions

    def update_sensors(self):
        for sensor_data in self.sensor_data:
            data = sensor_data["data"]
            if data.once:
                continue
            elif (data.last_checked - datetime.now).total_seconds() >= data.check_every:
                sensor_data.update(sensor_data["lambda"]())

class SensorData():
    def __init__(self, unit, last_value, once = False):
        self.last_checked =  datetime.now()
        self.once =  once
        self.uploaded_to_server = False
        self.last_value = last_value
        self.units  = unit #SI unit that measures the value given
    
    def update(self, new_data):
        #Update and add to queue if still not in server
        self.last_value = new_data

    
    def __str__(self):
        return "{} {} last updated at: {}".format(self.last_value, self.units, self.last_checked)