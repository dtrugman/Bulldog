"""
Defines the UnixService class
"""

import os
import signal
import logging
import lockfile
import daemon

from app.manager import Manager

class UnixService(object):
    """
    Unix service wrapper
    """

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config

    def start(self):
        """
        Start the service
        """
        context = daemon.DaemonContext()
        with context:
            Manager(self.config).start()
