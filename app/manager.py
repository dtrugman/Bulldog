"""
Defines the Manager class
"""

import sys
import logging
import threading

from app.config_parser import ConfigParser
from app.version import Version

from app.watchdog import Watchdog

class Manager(object):
    """
    Watchdogs manager
    """

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.stopped = threading.Event()

        self.mode = None
        self.config = None
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
        config_parser = ConfigParser(sys.argv)
        self.mode = config_parser.get_mode()
        self.config = config_parser.get_config()

        for app in self.config:
            self.watchdogs[app] = Watchdog(app, self.config[app])
            self.watchdogs[app].start()

    def _stop(self):
        if not self.config:
            return

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
            #self.stopped.wait()
            raw_input("")
        except Exception as err:
            self.logger.info("Error!\n%s", err)
        finally:
            self._stop()
            self._outro()

    def stop(self):
        """
        Stop module
        """
        self.stopped.set()
