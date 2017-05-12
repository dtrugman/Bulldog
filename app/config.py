"""
Defines the Config class
"""
import json
import os

class Config(object):
    """
    A class that is responsible for loading configuration
    """

    ARGS_EXPECTED = 2
    ARGS_EXE = 0
    ARGS_PATH = 1

    @staticmethod
    def load(argv):
        """
        Loads the configuration file specified by the command line arguments
        """
        if len(argv) != Config.ARGS_EXPECTED:
            raise RuntimeError("Usage: {0} <config>".format(argv[Config.ARGS_EXE]))

        path = argv[Config.ARGS_PATH]
        if not os.path.isfile(path):
            raise RuntimeError("Bad config file path [{0}] specified".format(path))

        config = {}
        with open(path) as jfile:
            config = json.load(jfile)

        return config
