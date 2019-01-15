import argparse, json, logging
from Helpers import plugged_sensor

currentSensors = []

def initialize_sensors(sensorList):
    for sensor in sensorList:
            global currentSensors
            if(sensor["type"] == "i2c"):
                currentSensors.append(plugged_sensor.PluggedSensor(sensor))

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('sensor.log')
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    parser = argparse.ArgumentParser(description="Choose parameters to be used with the sensor box")
    parser.add_argument("sensors", metavar='j', help="Choose json file with the description of the available sensors")
    parser.add_argument("debug", metavar='d', help="Choose to use dummy data")
    args = parser.parse_args()
    sensor_list = json.loads(args.sensors["sensors"])
    initialize_sensors(sensor_list)