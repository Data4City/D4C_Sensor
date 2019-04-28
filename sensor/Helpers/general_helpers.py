import argparse
import logging


def find_occurence_in_list(list_to_check: list, condition):
    return next((obj for obj in list_to_check if condition), {})


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


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
