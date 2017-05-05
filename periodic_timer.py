"""
Defines the PeriodicTimer class
"""

import logging
import threading

class PeriodicTimer(object):
    """
    A simple periodic Timer
    that executes an action each time it's triggered
    """

    def __init__(self, freq, action, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.freq = freq
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.timer = None

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _trigger(self):
        self.logger.info("Executing")
        self.action(*self.args, **self.kwargs)
        self._register()

    def _register(self):
        self.timer = threading.Timer(self.freq, self._trigger)
        self.timer.start()

    def stop(self):
        """
        Stop the periodic timer
        """
        self.timer.cancel()
        self._outro()

    def start(self):
        """
        Start the periodic timer
        It will execute the specified action every 'freq' seconds
        """
        self._intro()
        self._register()
