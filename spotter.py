"""
Defines the Spotter class
"""

import logging
import psutil

from config import ConfigParser

class Spotter(object):
    """
    A class for spotting target processes
    """

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)

        self._configure(config) # Must come first after logger init

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            self.logger.info("Configuration:")

            # Save original config
            self.config = config

            # Get cmd
            self.cmdline = ConfigParser.parse_cmdline(config)
            self.logger.info("Target cmdline: %s", self.cmdline)
        except KeyError as err:
            raise RuntimeError("Bad Spotter configuration: " + str(err))

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def get_targets(self):
        """
        Get all running target processes
        """
        return [proc for proc in psutil.process_iter() if proc.cmdline() == self.cmdline]

