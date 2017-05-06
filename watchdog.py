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
        config = Config.load()

        self.handler = Handler(config["target"],
                               config["handler"])
        self.handler.start()

        self.investigator = Investigator(config["target"],
                                         config["investigator"],
                                         self.handler)
        self.investigator.start()

        self.cycler = Cycler(config["cycler"],
                             self.investigator)
        self.cycler.start()

    def _stop(self):
        self.cycler.stop()

        self.investigator.stop()

        self.handler.stop()

    def run(self):
        try:
            self._intro()
            self._run()
            self.stopped.wait(30) # Fake 30 sec run
            self._stop()
        except Exception as ex:
            self.logger.error(ex.message)
        finally:
            self._outro()

    def stop(self):
        self.stopped.set()
