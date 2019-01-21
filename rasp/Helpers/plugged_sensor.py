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
        
        self.type = "i2c"
        self.name = sensor["name"]
        self.model = sensor["model"]
        self.sensor_data = self.construct_sensor_data(sensor["data"]) #List containing Sensor Data objects

    
    def construct_sensor_data(self, data):
        data = []
        for unit in data:
            currLambda = lambda: getattr(self.__sensor__, unit["function"])
            data.append( 
                SensorData(
                unit = unit["unit"], 
                last_value=currLambda(), 
                data_lambda = currLambda),
                once = unit["once"],
            )
        return data

    def update_sensors(self) -> bool:
        """Tries to update the sensors and if it's successful it returns a boolean if any sensor gets updated"""
        result = False
        for sensor_data in self.sensor_data:
            data = sensor_data["data"]
            
            if (data.last_checked - datetime.now).total_seconds() >= data.check_every:
                #Check if the difference is big enough to merit a change
                delta = abs(data.last_value * 0.05)
                current = sensor_data.function()
                if data.last_value + delta > current or data.last_value  - delta < current:
                    sensor_data.update()
                    result = True
        
        return result

    def __post_data__(self, sensor_idx: int = None) -> dict:
        if not sensor_idx: 
            return {"name": self.name , "model": self.model}
        else: 
            return {"name": self.name , "model": self.model, "data": self.sensor_data[sensor_idx]}


class SensorData():
    def __init__(self, unit, last_value, data_lambda,  once = False):
        self.timestamp =  datetime.now()
        self.once =  once
        self.last_value = last_value
        self.units  = unit #SI unit that measures the value given
        self.function = data_lambda
        self.enqueued = False

    def update(self):
        #Update and add to queue if still not in server
        if not self.once:
            self.last_value = self.function()
            self.timestamp = datetime.now()
            self.enqueued = False
    
    def __str__(self):
        return "{} {} last updated at: {}".format(self.last_value, self.units, self.last_checked)
    
    def __post_data(self):
        return {"timestamp": self.timestamp, "value": self.last_value}