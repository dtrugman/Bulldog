"""
Defines the UnixService class
"""

import os
import daemon # Reference: https://github.com/arnaudsj/python-daemon
import daemon.pidfile

from app.globals import Globals
from app.manager import Manager

class UnixService(object):
    """
    Unix service wrapper
    """

    @staticmethod
    def start(config):
        """
        Start the service
        """
        context = daemon.DaemonContext()
        context.working_directory = os.getcwd()
        context.pidfile = daemon.pidfile.TimeoutPIDLockFile(Globals.PID_FILE,
                                                            Globals.PID_ACQUIRE_TIMEOUT)
        with context:
            Manager.run(config)
