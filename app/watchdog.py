"""
Defines the Watchdog class
"""

import logging
import threading

from app.cycler import Cycler
from app.inspector import Inspector
from app.handler import Handler

class Watchdog(object):
    """
    A watchdog that monitors a single application
    """

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)

        self.stopped = threading.Event()

        self.config = config

        self.cycler = None
        self.inspector = None
        self.handler = None

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _run(self):
        self.handler = Handler(self.config["handler"])
        self.handler.start()

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

        if self.handler:
            self.handler.stop()

    def start(self):
        """
        Start watchdog
        """
        try:
            self._intro()
            self._run()
            self.stopped.wait()
        except Exception as ex:
            self.logger.error(ex.message)
        finally:
            self._stop()
            self._outro()

    def stop(self):
        """
        Stop watchdog
        """
        self.stopped.set()
