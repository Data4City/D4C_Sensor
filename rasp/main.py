import argparse, json, logging, busio, board, asyncio
from Helpers import plugged_sensor, requests_handler
from Helpers import redis_helper as rh
current_plugged_sensors = []
def initialize_sensors(sensorList):
    i2c = busio.I2C(board.SCL, board.SDA)

    for sensor in sensorList["sensors"]:
            global current_plugged_sensors
            if(sensor["type"] == "i2c"):
                current_plugged_sensors.append(plugged_sensor.PluggedSensor(sensor, i2c))

async def sense():
    while True:
        print("sensing")
        for sensor in current_plugged_sensors:
            if sensor.update_sensors():
                if sensor.type == "i2c":
                    for i,data in enumerate(sensor.sensor_data):
                        if not data.enqueued:
                            requests_handler.post_sensor.delay(sensor.__post_data__(i))
                            data.enqueued = True
                elif sensor.type == "mic":
                    print("Microphone check")
        await asyncio.sleep(5)



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


            asyncio.ensure_future(sense())
            # asyncio.ensure_future(rh.process_workers())
            
            asyncio.get_event_loop().run_forever()


            from Helpers import flask_helper
            flask_helper.start()

    except FileNotFoundError:
        print("wat")
        logger.error("File sensor settings file ({}) doesn't exist".format(args.sensors))
    except Exception as e:
        print(e)
