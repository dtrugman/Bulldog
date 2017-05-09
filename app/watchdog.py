"""
Defines the WatchDog class
"""

import sys
import logging
import threading

from app.config import Config
from app.version import Version

from app.cycler import Cycler
from app.inspector import Inspector
from app.handler import Handler

class WatchDog(object):
    """
    Main watchdog object
    """

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.stopped = threading.Event()

        self.config = None
        self.cycler = None
        self.inspector = None
        self.handler = None

    def _intro(self):
        self.logger.info("Starting")
        self.logger.info("-----------------------------------------------")
        self.logger.info("Version: %s", Version.VERSION)
        self.logger.info("Build:   %s", Version.BUILD)
        self.logger.info("-----------------------------------------------")

    def _outro(self):
        self.logger.info("Stopped")

    def _run(self):
        self.config = Config(sys.argv)

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
        Start watchdog module
        """
        try:
            self._intro()
            self._run()
            #self.stopped.wait()
            raw_input("")
        except Exception as ex:
            self.logger.error(ex.message)
        finally:
            self._stop()
            self._outro()

    def stop(self):
        """
        Stop watchdog module
        """
        self.stopped.set()
