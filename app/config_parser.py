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
    def _check(config):
        if not config:
            raise RuntimeError("Bad config file[{0}], BLA BLA...")
        return True

    @staticmethod
    def load(path):
        """
        Loads the configuration file specified by the command line arguments
        """
        if not os.path.isfile(path):
            raise RuntimeError("Bad config file path[{0}] specified".format(path))

        config = {}
        with open(path) as jfile:
            config = json.load(jfile)

        # Throws RuntimeError if not valid
        ConfigParser._check(config)

        return config
