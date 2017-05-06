import logging
import threading

from config import Config
from config import Globals

from cycler import Cycler
from investigator import Investigator

class WatchDog(object):

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.stopped = threading.Event()

        self.cycler = None
        self.investigator = None

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

        self.investigator = Investigator(config)
        self.investigator.start()

        self.cycler = Cycler(config["cycler"], self.investigator)
        self.cycler.start()

    def _stop(self):
        self.cycler.stop()

        self.investigator.stop()

    def run(self):
        try:
            self._intro()
            self._run()
            self.stopped.wait(3) # Fake 3 sec run
            self._stop()
        except Exception as ex:
            self.logger.error(ex.message)
        finally:
            self._outro()

    def stop(self):
        self.stopped.set()
