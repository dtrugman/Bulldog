"""
Defines the Config Parser class
"""
import json
import os

class ConfigParser(object):
    """
    A class that is responsible for loading configuration
    """

    ARGS_EXPECTED = 3
    ARGS_EXE = 0
    ARGS_MODE = 1
    ARGS_PATH = 2

    MODE_SERVICE = "service"
    MODE_APP = "app"

    def __init__(self, argv):
        self._parse(argv)

    def _hint(self, error=""):
        hint = "Usage: {0} ({1}|{2}) <config-file>".format(
            self.argv[ConfigParser.ARGS_EXE],
            ConfigParser.MODE_SERVICE,
            ConfigParser.MODE_APP)
        if error:
            hint = error + "\n" + hint
        return hint

    def _parse(self, argv):
        """
        Loads the configuration file specified by the command line arguments
        """
        self.argv = argv

        if len(argv) != ConfigParser.ARGS_EXPECTED:
            hint = self._hint()
            raise RuntimeError(hint)

        self.mode = argv[ConfigParser.ARGS_MODE]
        if self.mode != ConfigParser.MODE_SERVICE and self.mode != ConfigParser.MODE_APP:
            hint = self._hint("Bad mode[{0}] specified".format(self.mode))
            raise RuntimeError(hint)

        path = argv[ConfigParser.ARGS_PATH]
        if not os.path.isfile(path):
            hint = self._hint("Bad config file[{0}] specified".format(path))
            raise RuntimeError(hint)

        self.config = {}
        with open(path) as jfile:
            self.config = json.load(jfile)

    def get_mode(self):
        """
        Get the underlying mode
        """
        return self.mode

    def get_config(self):
        """
        Get the underlying config
        """
        return self.config
