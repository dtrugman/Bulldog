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

    def __init__(self, target_name, freq, action, *args, **kwargs):
        self.target_name = target_name
        self.logger = logging.getLogger(self.target_name)
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
        self.logger.debug("Triggered")
        self.action(*self.args, **self.kwargs)
        self._register()

    def _register(self):
        self.timer = threading.Timer(self.freq, self._trigger)
        self.timer.start()

    def stop(self):
        """
        Stop the periodic timer
        """
        if self.timer:
            self.timer.cancel()
        self._outro()

    def start(self):
        """
        Start the periodic timer
        It will execute the specified action every 'freq' seconds
        """
        self._intro()
        self._register()
