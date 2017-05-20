"""
Defines the Manager class
"""

import logging
import threading

from app.config_parser import ConfigParser
from app.globals import Globals
from app.version import Version
from app.watchdog import Watchdog

class Manager(object):
    """
    Watchdogs` manager
    """

    def __init__(self, config):
        self.config = config

        self._init_log()

        self.stopped = threading.Event()

        self.watchdogs = {}

    def _init_log(self):
        log_config = self.config[ConfigParser.KEY_LOG]

        log_dir = log_config[ConfigParser.KEY_DIR]
        log_file = log_dir + '/' + Globals.LOG_FILE

        log_level = log_config[ConfigParser.KEY_LEVEL]

        log_format = Globals.LOG_FORMAT

        logging.basicConfig(level=log_level,
                            filename=log_file,
                            format=log_format)
        self.logger = logging.getLogger(__name__)

    def _intro(self):
        self.logger.critical("=============================")
        self.logger.critical("Starting")
        self.logger.critical("-----------------------------")
        self.logger.critical("Version: %s", Version.VERSION)
        self.logger.critical("Build:   %s", Version.BUILD)
        self.logger.critical("=============================")

    def _outro(self):
        self.logger.critical("=============================")
        self.logger.critical("Stopped")
        self.logger.critical("=============================\n\n\n")

    def _run(self):
        watchdogs = self.config[ConfigParser.KEY_WATCHDOGS]
        for app in watchdogs:
            self.watchdogs[app] = Watchdog(app, watchdogs[app])
            self.watchdogs[app].start()

    def _stop(self):
        watchdogs = self.config[ConfigParser.KEY_WATCHDOGS]
        for app in watchdogs:
            if self.watchdogs[app]:
                self.watchdogs[app].stop()
                self.watchdogs[app].join()

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
