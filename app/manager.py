"""
Defines the Manager class
"""

import signal
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
        self.logger = logging.getLogger('global')

    def _intro(self):
        self.logger.critical("==================================")
        self.logger.critical("Starting")
        self.logger.critical("----------------------------------")
        self.logger.critical("Version: %s", Version.VERSION)
        self.logger.critical("Build:   %s", Version.BUILD)
        self.logger.critical("==================================")

    def _outro(self):
        self.logger.critical("==================================")
        self.logger.critical("Stopped")
        self.logger.critical("==================================\n\n\n")

    def _start(self):
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
        self._intro()
        self._start()

    def stop(self):
        """
        Stop module
        """
        self._stop()
        self._outro()

    @staticmethod
    def run(config):
        """
        This is a static wrapper around manager
        It handles signals and graceful termination
        """
        try:
            manager = Manager(config)
            manager.start()
            signal.pause()
        except (KeyboardInterrupt, SystemExit):
            manager.stop()
