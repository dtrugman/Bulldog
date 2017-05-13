"""
Defines the Config Parser class
"""
import json
import os

class ConfigParser(object):
    """
    A class that is responsible for loading configuration
    """

    @staticmethod
    def load(path):
        """
        Loads the configuration file specified by the command line arguments
        """
        if not os.path.isfile(path):
            raise RuntimeError("Bad config file[{0}] specified".format(path))

        config = {}
        with open(path) as jfile:
            config = json.load(jfile)
        return config
