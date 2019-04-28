import sys


def create_config(config):
    config_module = sys.modules[__name__]

    for k, v in config.items():
        setattr(config_module, k, v)

    delattr(config_module, "sys")
