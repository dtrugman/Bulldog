"""
Defines the Runner class
"""

import platform

from app.unix_service import UnixService
from app.win_service import WinService
from app.manager import Manager

class Runner(object):
    """
    A class for running a the app
    """

    @staticmethod
    def _run_app(config_path):
        Manager(config_path).start()

    @staticmethod
    def _run_service(config_path):
        if platform.system() == "Linux":
            UnixService.start(config_path)
        elif platform.system() == "Windows":
            WinService.start(config_path)
        else:
            raise RuntimeError("Unsupported platform")

    @staticmethod
    def run(service, config_path):
        """
        Run the application
        """
        try:
            if service:
                Runner._run_service(config_path)
            else:
                Runner._run_app(config_path)
        except Exception as err:
            print "Error: {0}".format(err)
