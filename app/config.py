"""
Defines the Globals, Config and ConfigParsers classes
"""
import json
import os

class Globals(object):
    """
    A class that holds project wide global values
    """

    VERSION = "0.0.1"
    BUILD = 999999


class Config(object):
    """
    A class that is responsible for loading configuration
    """

    ARGS_EXPECTED = 2
    ARGS_EXE = 0
    ARGS_PATH = 1

    def __init__(self, argv):
        if len(argv) != Config.ARGS_EXPECTED:
            raise RuntimeError("Usage: {0} <config>".format(argv[Config.ARGS_EXE]))

        path = argv[Config.ARGS_PATH]
        if not os.path.isfile(path):
            raise RuntimeError("Bad config file path [{0}] specified".format(path))

        self.config = {}
        with open(path) as jfile:
            self.config = json.load(jfile)

    def __getitem__(self, key):
        return self.config[key]
