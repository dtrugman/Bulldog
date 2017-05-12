"""
Defines the Runner class
"""

import sys
import platform

from app.config_parser import ConfigParser
from app.unix_service import UnixService
from app.win_service import WinService
from app.manager import Manager

class Runner(object):
    """
    A class for running a the app
    """

    def __init__(self):
        pass

    def _app(self, config):
        Manager(config).start()

    def _service(self, config):
        if platform.system() == "Linux":
            UnixService(config).start()
        elif platform.system() == "Windows":
            WinService(config).start()
        else:
            raise RuntimeError("Unsupported platform")

    def run(self):
        """
        Run the application
        """
        try:
            config_parser = ConfigParser(sys.argv)
            mode = config_parser.get_mode()
            config = config_parser.get_config()

            if mode == ConfigParser.MODE_APP:
                self._app(config)
            elif mode == ConfigParser.MODE_SERVICE:
                self._service(config)
            else: # We should never reach this because ConfigParser validates it
                raise RuntimeError("Config error")
        except Exception as err:
            print "Error: {0}".format(err)
