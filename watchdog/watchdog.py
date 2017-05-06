import sys
import logging
import threading

from config import Config
from config import Globals

from cycler import Cycler
from investigator import Investigator
from handler import Handler

class WatchDog(object):

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.stopped = threading.Event()

        self.config = None
        self.cycler = None
        self.investigator = None
        self.handler = None

    def _intro(self):
        self.logger.info("-----------------------------------------------")
        self.logger.info("Starting")
        self.logger.info("-----------------------------------------------")
        self.logger.info("Version: %s", Globals.VERSION)
        self.logger.info("Build:   %d", Globals.BUILD)
        self.logger.info("-----------------------------------------------")

    def _outro(self):
        self.logger.info("Stopped")

    def _run(self):
        self.config = Config(sys.argv)

        self.handler = Handler(self.config["handler"])
        self.handler.start()

        self.investigator = Investigator(self.config["investigator"],
                                         self.handler)
        self.investigator.start()

        self.cycler = Cycler(self.config["cycler"],
                             self.investigator)
        self.cycler.start()

    def _stop(self):
        if self.cycler:
            self.cycler.stop()

        if self.investigator:
            self.investigator.stop()

        if self.handler:
            self.handler.stop()

    def run(self):
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
        self.stopped.set()
