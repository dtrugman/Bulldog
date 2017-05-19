"""
Defines the Manager class
"""

import logging
import threading

from app.globals import Globals
from app.version import Version
from app.watchdog import Watchdog

class Manager(object):
    """
    Watchdogs` manager
    """

    def __init__(self, config):
        self.config = config

        logging.basicConfig(level=logging.DEBUG,
                            filename=Globals.LOG_FILE,
                            format=Globals.LOG_FORMAT)
        self.logger = logging.getLogger(__name__)

        self.stopped = threading.Event()

        self.watchdogs = {}

    def _intro(self):
        self.logger.info("Starting")
        self.logger.info("-----------------------------------------------")
        self.logger.info("Version: %s", Version.VERSION)
        self.logger.info("Build:   %s", Version.BUILD)
        self.logger.info("-----------------------------------------------")

    def _outro(self):
        self.logger.info("Stopped")

    def _run(self):
        for app in self.config:
            self.watchdogs[app] = Watchdog(app, self.config[app])
            self.watchdogs[app].start()

    def _stop(self):
        for app in self.config:
            if self.watchdogs[app]:
                self.watchdogs[app].stop()

    def start(self):
        """
        Start module
        """
        try:
            self._intro()
            self._run()
            self.stopped.wait()
        except Exception as err:
            self.logger.error("Error!\n%s", err)
        finally:
            self._stop()
            self._outro()

    def stop(self):
        """
        Stop module
        """
        self.stopped.set()
