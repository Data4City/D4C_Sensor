import argparse, json, logging, busio, board
import requests_handler

from Helpers import plugged_sensor


current_plugged_sensors = []

def initialize_sensors(sensorList):
    i2c = busio.I2C(board.SCL, board.SDA)

    for sensor in sensorList["sensors"]:
            global current_plugged_sensors
            if(sensor["type"] == "i2c"):
                current_plugged_sensors.append(plugged_sensor.PluggedSensor(sensor, i2c))

def sense():
    for sensor in current_plugged_sensors:
              if sensor.update_sensors:
                if sensor.type == "i2c":
                  for i,data in enumerate(sensor.data):
                      if not data.enqueued:
                          requests_handler.post_sensor(data.__post_data(i))
                          data.enqueued = True
                elif sensor.type == "mic":
                    print("Microphone check")



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
    parser.add_argument("--debug", metavar='-d', help="Choose to use dummy data", default=False)
    args = parser.parse_args()

    try:
        with open(args.sensors) as f: 
            sensor_list = json.load(f)
            initialize_sensors(sensor_list)
            from Helpers import redis_helper
            redis_helper.scheduler.cron("*/5 * * * *", func=sense, repeat=None,queue_name="update_sensor")
    except FileNotFoundError:
        logger.error("File sensor settings file ({}) doesn't exist".format(args.sensors))
