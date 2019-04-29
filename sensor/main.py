import argparse, yaml, logging
from .Helpers.general_helpers import get_serial, str2bool
from sensor import config

# TODO separate logic from worker into separate file and service
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
    args = parser.parse_args()

    try:
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
