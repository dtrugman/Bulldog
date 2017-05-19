"""
Defines the Watchdog class
"""

import logging
import threading

from app.cycler import Cycler
from app.inspector import Inspector
from app.handler import Handler

class Watchdog(threading.Thread):
    """
    A watchdog that monitors a single application
    """

    def __init__(self, name, config):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)

        self.stopped = threading.Event()

        self.name = name
        self.config = config

        self.cycler = None
        self.inspector = None
        self.handler = None

    def _intro(self):
        self.logger.info("Starting to monitor %s", self.name)

    def _outro(self):
        self.logger.info("Stopped")

    def _run(self):
        self.handler = Handler(self.config["handler"])

        self.inspector = Inspector(self.config["inspector"],
                                   self.handler)
        self.inspector.start()

        self.cycler = Cycler(self.config["cycler"],
                             self.inspector)
        self.cycler.start()

    def _stop(self):
        if self.cycler:
            self.cycler.stop()

        if self.inspector:
            self.inspector.stop()

    def run(self):
        self._intro()
        self._run()
        self.stopped.wait()
        self._stop()
        self._outro()

    def stop(self):
        """
        Stop watchdog
        """
        self.stopped.set()
