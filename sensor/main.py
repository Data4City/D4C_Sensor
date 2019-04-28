import argparse, yaml, logging
from .Helpers.general_helpers import get_serial, str2bool
from sensor import config

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
    parser.add_argument("--worker", metavar='-w', nargs='?', type=str2bool, help="Run the queue worker?", default=True)
    args = parser.parse_args()

    try:

        if args.worker:
            if args.worker:
                from sensor.Helpers import rq_worker
                from dashboard.app import flask_helper

                rq_worker.process_workers(config.rq_worker["queues"])
        else:
            with open(args.sensors, 'r') as f:
                try:
                    from sensor.raspberry_handler import Raspy

                    config.create_config(config=yaml.safe_load(f))
                    rasp = Raspy(get_serial())
                    rasp.run()

                except yaml.YAMLError as exc:
                    logger.error(exc)

    except FileNotFoundError:
        logger.error("File sensor settings file ({}) doesn't exist".format(args.sensors))
