import argparse


def find_occurence_in_list(list_to_check: list, condition):
    return next((obj for obj in list_to_check if condition), {})


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')