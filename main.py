import argparse, yaml, logging
from threading import Thread
from raspberry_handler import Raspy

from Helpers.general_helpers import str2bool


def get_serial(serial="0000000000000000"):
    # Extract serial from cpuinfo file
    if serial == "0000000000000000" or serial == "ERROR000000000":
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line[0:6] == 'Serial':
                        serial = line[10:26]
        except:
            logger = logging.getLogger(__name__)
            logger.error("Serial number not found")
            serial = "ERROR000000000"
    return serial


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('sensor.log')
    logging.getLogger().setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser(description="Choose parameters to be used with the sensor box")
    parser.add_argument("--sensors", metavar='-j',
                        help="Choose json file with the description of the available sensors",
                        default="config.yaml")
    parser.add_argument("--flask", metavar='-f', nargs='?', type=str2bool, help="Run flask in background?",
                        default=True)
    parser.add_argument("--worker", metavar='-w', nargs='?', type=str2bool, help="Run the queue worker?", default=True)
    args = parser.parse_args()

    try:
        with open(args.sensors) as f:
            config = yaml.safe_load(f)
            rasp = Raspy(get_serial(), config)

            if args.flask:
                from Helpers import flask_helper

                flask_thread = Thread(target=flask_helper.start)
                flask_thread.start()

            if args.worker:
                from Helpers import rq_worker

                rq_worker.process_workers(config["rq_worker"]["queues"])

    except FileNotFoundError:
        logger.error("File sensor settings file ({}) doesn't exist".format(args.sensors))
