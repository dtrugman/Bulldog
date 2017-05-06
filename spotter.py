"""
Defines the Spotter class
"""

import logging
import psutil

class Spotter(object):
    """
    A class for spotting target processes
    """

    KEY_CMD = "cmd"
    KEY_ARGS = "args"

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
            self.cmd = self.config[Spotter.KEY_CMD]
            self.logger.info("Target cmd: %s", self.cmd)

            # Get args
            self.args = self.config[Spotter.KEY_ARGS]
            self.logger.info("Target args: %s", self.args)

            # Build cmdline list
            # We append an empty string('') when the args are empty
            # because psutil does the same
            self.cmdline = []
            self.cmdline.append(self.cmd)
            self.cmdline.append('' if len(self.args) == 0 else self.args)
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

