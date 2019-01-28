import argparse, json, logging
from threading import Thread
import raspberry_handler as rh

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('sensor.log')
    logging.getLogger().setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    parser = argparse.ArgumentParser(description="Choose parameters to be used with the sensor box")
    parser.add_argument("--sensors", metavar='-j', help="Choose json file with the description of the available sensors", default = "sensorList.json")
    parser.add_argument("--flask", metavar='-f', help="Run flask in background?", default=True)
    parser.add_argument("--worker", metavar='-w', help="Run the queu worker?", default=True)
    args = parser.parse_args()
    try:
        with open(args.sensors) as f: 
            sensor_list = json.load(f)
            
            rh.init_rasp(sensor_list)

            if(args.flask):
                from Helpers import flask_helper
                flask_thread = Thread(target = flask_helper.start)
                flask_thread.start()

            if(args.worker):
                from Helpers import redis_helper
                redis_helper.process_workers()
            
          #  f.close()
    except FileNotFoundError:
        print("wat")
        logger.error("File sensor settings file ({}) doesn't exist".format(args.sensors))
