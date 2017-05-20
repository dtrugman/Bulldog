"""
Defines the Watchdog class
"""

import logging
import threading

from app.triggers.time.cycler import Cycler
from app.triggers.http.rest import RestService

from app.inspector import Inspector
from app.handler import Handler

class Watchdog(threading.Thread):
    """
    A watchdog that monitors a single application
    """

    KEY_HANDLER = "handler"
    KEY_INSPECTOR = "inspector"
    KEY_TRIGGERS = "triggers"
    KEY_CYCLER = "cycler"
    KEY_REST = "rest"

    def __init__(self, target_name, config):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(target_name)

        self.stopped = threading.Event()

        self.target_name = target_name
        self.config = config

        self.cycler = None
        self.rest_service = None

        self.inspector = None
        self.handler = None

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _run(self):
        self.handler = Handler(self.target_name,
                               self.config[Watchdog.KEY_HANDLER])

        self.inspector = Inspector(self.target_name,
                                   self.config[Watchdog.KEY_INSPECTOR],
                                   self.handler)
        self.inspector.start()

        triggers = self.config[Watchdog.KEY_TRIGGERS]

        if Watchdog.KEY_CYCLER in triggers:
            self.cycler = Cycler(self.target_name,
                                 triggers[Watchdog.KEY_CYCLER],
                                 self.inspector)
            self.cycler.start()

        if Watchdog.KEY_REST in triggers:
            self.rest_service = RestService(self.target_name,
                                            triggers[Watchdog.KEY_REST],
                                            self.inspector)
            self.rest_service.start()

    def _stop(self):
        if self.cycler:
            self.cycler.stop()

        if self.inspector:
            self.inspector.stop()

    def run(self):
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
        Stop watchdog
        """
        self.stopped.set()
