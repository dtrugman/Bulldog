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

    KEY_CMD = "cmd"
    KEY_ARGS = "args"

    CMD_LINE_ITEM = [KEY_CMD, KEY_ARGS]

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

class ConfigParser(object):
    """
    A static class that is responsible for parsing and
    validating common configuration
    """

    @staticmethod
    def parse_cmdline(value):
        """
        Parses a value that is expected to contain a complete command line
        """

        if len(value) != len(Config.CMD_LINE_ITEM):
            raise KeyError("Command line item misconfigured")

        for item in value:
            if item not in Config.CMD_LINE_ITEM:
                raise KeyError("Command line bad key[{0}]".format(item))

        if not isinstance(value[Config.KEY_CMD], basestring):
            raise KeyError("Command line item bad key[{0}] value: "
                           "non-string".format(Config.KEY_CMD))

        if not isinstance(value[Config.KEY_ARGS], list):
            raise KeyError("Command line item bad key[{0}] value: "
                           "not a list".format(Config.KEY_ARGS))

        for item in value[Config.KEY_ARGS]:
            if not isinstance(item, basestring):
                raise KeyError("Command line item bad key[{0}] value: "
                               "contains non-string".format(Config.KEY_ARGS))

        cmdline = [value[Config.KEY_CMD]]
        if value[Config.KEY_ARGS]:
            cmdline += value[Config.KEY_ARGS]
        else:
            cmdline += [''] # We append an empty string to be compatible with psutil
        return cmdline
