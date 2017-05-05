"""
Defines the Cycler class
"""

import logging

from periodic_timer import PeriodicTimer

class Cycler(object):
    """
    A simple object that uses a periodic timer and
    pushes investigation requests each time it's triggered
    """

    def __init__(self, config, investigator):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.investigator = investigator
        self.periodic_timer = PeriodicTimer(self.config["freq"], self._trigger)

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _trigger(self):
        manifest = self.config["manifest"]
        for item in manifest:
            for check in item["check"]:
                self.logger.info("Enqueuing request: %s", check)
                self.investigator.enqueue(check)

    def stop(self):
        """
        Stop the cycler
        """
        self.periodic_timer.stop()
        self._outro()

    def start(self):
        """
        Start the cycler.
        It will execute the specified action every 'freq' seconds
        """
        self._intro()
        self.periodic_timer.start()
