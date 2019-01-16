import argparse, json, logging, busio, board
from Helpers import plugged_sensor
currentSensors = []

def initialize_sensors(sensorList):
    i2c = busio.I2C(board.SCL, board.SDA)

    for sensor in sensorList["sensors"]:
            global currentSensors
            if(sensor["type"] == "i2c"):
                currentSensors.append(plugged_sensor.PluggedSensor(sensor, i2c))

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('sensor.log')
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    parser = argparse.ArgumentParser(description="Choose parameters to be used with the sensor box")
    parser.add_argument("--sensors", metavar='-j', help="Choose json file with the description of the available sensors", default = "sensorList.json")
    parser.add_argument("--debug", metavar='-d', help="Choose to use dummy data", default=False, required= False)
    args = parser.parse_args()
    try:
        with open(args.sensors) as f: 
            sensor_list = json.load(f)
            initialize_sensors(sensor_list)
            

            # TODO delete this and create async CRON job that'll update sensors
            for i in currentSensors:
                for sensor_data in i.sensor_data:
                    print(sensor_data["data"])
        
    except FileNotFoundError:
        logger.error("File doesn't exist")