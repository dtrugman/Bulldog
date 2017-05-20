"""
Defines the Runner class
"""

import platform

from app.config_parser import ConfigParser
from app.unix_service import UnixService
from app.win_service import WinService
from app.manager import Manager

class Runner(object):
    """
    A class for running a the app
    """

    @staticmethod
    def _run_app(config):
        print "Running as application"
        manager = Manager(config)
        manager.start()
        raw_input("Press any key to terminate")
        manager.stop()

    @staticmethod
    def _run_service(config):
        print "Running as service"
        if platform.system() == "Linux":
            UnixService.start(config)
        elif platform.system() == "Windows":
            WinService.start(config)
        else:
            raise RuntimeError("Unsupported platform")

    @staticmethod
    def run(service, config_path):
        """
        Run the application
        """
        try:
            config = ConfigParser.load(config_path)

            if service:
                Runner._run_service(config)
            else:
                Runner._run_app(config)
        except Exception as err:
            print "Error: {0}".format(err)
