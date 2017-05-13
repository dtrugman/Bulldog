"""
Defines the UnixService class
"""

import os
import signal
import lockfile
import daemon

from app.manager import Manager

class UnixService(object):
    """
    Unix service wrapper
    """

    @staticmethod
    def start(config_path):
        """
        Start the service
        """
        context = daemon.DaemonContext(
            working_directory=os.getcwd()
        )
        with context:
            Manager(config_path).start()
