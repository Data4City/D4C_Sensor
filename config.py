import sys

import yaml
#TODO WOrk on global config

def create_config(f):
    config = yaml.safe_load(f)
    for k, v in config.items():
        setattr(sys.modules["config"], k, v)
