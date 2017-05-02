"""
Defines the Cycler class
"""

import logging
import threading

class Cycler(object):
    """
    A simple object that works as a periodic timer
    and executes an action each time it's triggered
    """

    def __init__(self, freq, action, *args, **kwargs):
        self.logger = logging.getLogger('watchdog')
        self.freq = freq
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.timer = None

    def _intro(self):
        self.logger.info("Cycler starting")

    def _outro(self):
        self.logger.info("Cycler stopped")

    def _trigger(self):
        self.logger.info("Cycler executing")
        self.action(*self.args, **self.kwargs)
        self._register()

    def _register(self):
        self.timer = threading.Timer(self.freq, self._trigger)
        self.timer.start()

    def stop(self):
        """
        Stop the cycler
        """
        self.timer.cancel()
        self._outro()

    def start(self):
        """
        Start the cycler.
        It will execute the specified action every 'freq' seconds
        """
        self._intro()
        self._register()
