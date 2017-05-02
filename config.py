import json
import os

class Globals:
    """A class that holds project wide global values
    """

    VERSION = "0.0.1"
    BUILD = 999999


class Config:
    """A class that is responsible for loading and handling configuration
    """

    config = {}

    @classmethod
    def load(cls, argv):
        args_expected = 2
        args_exe = 0
        args_path = 1

        if len(argv) != args_expected:
            raise RuntimeError("Usage: {0} <config>".format(argv[args_exe]))

        path = argv[args_path]
        if not os.path.isfile(path):
            raise RuntimeError("Bad config file path [{0}] specified".format(path))

        with open(path) as jfile:
            cls.config = json.load(jfile)

        return cls.config
