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

    
    def construct_sensor_data(self, sensor_data):
        data = []
        for unit_sensor in sensor_data:
            currLambda = lambda: getattr(self.__sensor__, unit_sensor["function"])
            sensor = SensorData(unit_sensor,currLambda)            
            data.append( sensor)
        return data

    def update_sensors(self) -> bool:
        """Tries to update the sensors and if it's successful it returns a boolean if any sensor gets updated"""
        result = False
        for data in self.sensor_data:
            if (datetime.now() - data.timestamp ).total_seconds() >= data.check_every:
                #Check if the difference is big enough to merit a change
                delta = abs(data.last_value * data.threshold)
                current = round(data.function(),2)
                if data.last_value + delta > current or data.last_value  - delta < current:
                    data.update()
                    result = True
        
        return result

    def __str__(self):
        return "{} {} {} \n{} ".format(self.name, self.type, self.model, ' '.join(str(sensor) for sensor in self.sensor_data))
    
    def __post_data__(self, sensor_idx: int = None) -> dict:
        if sensor_idx is None and sensor_idx == 0: 
            return {"name": self.name , "model": self.model}
        else: 
            return {"name": self.name , "model": self.model, "data": self.sensor_data[sensor_idx].__post_data__()}


class SensorData():
    def __init__(self, unit_sensor, data_lambda):
        self.timestamp =  datetime.now()
        self.once =  unit_sensor["once"]
        self.check_every = unit_sensor["check_every"]
        self.threshold = unit_sensor["threshold"]
        self.units  = unit_sensor["unit"] #SI unit that measures the value given
        self.last_value = data_lambda()
        self.function = data_lambda
        self.enqueued = False

    def update(self):
        #Update and add to queue if still not in server
        if not self.once:
            self.last_value = round(self.function(),2)
            self.timestamp = datetime.now()
            self.enqueued = False
    
    def __str__(self):
        return "{} {} last updated at: {}\n".format(self.last_value, self.units, self.timestamp)
    
    def __post_data__(self):
        return {"timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'), "value": self.last_value, "units": self.units}