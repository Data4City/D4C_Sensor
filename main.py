import argparse, yaml, logging
from threading import Thread
from Helpers.general_helpers import str2bool, get_serial
import config

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
        with open(args.sensors, 'r') as f:
            try:
                from raspberry_handler import Raspy

                config.create_config(config=yaml.safe_load(f))
                rasp = Raspy(get_serial())
                rasp.start()

                if args.flask:
                    from Helpers import flask_helper

                    flask_thread = Thread(target=flask_helper.start, name="Flask")
                    flask_thread.start()

                if args.worker:
                    from Helpers import rq_worker

                    rq_worker.process_workers(config.rq_worker["queues"])
            except yaml.YAMLError as exc:
                logger.error(exc)

    except FileNotFoundError:
        logger.error("File sensor settings file ({}) doesn't exist".format(args.sensors))
