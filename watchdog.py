import logging
import threading

from config import Config
from config import Globals

from cycler import Cycler

class WatchDog(object):

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.cycler = None

    def _intro(self):
        self.logger.info("-----------------------------------------------")
        self.logger.info("Starting")
        self.logger.info("-----------------------------------------------")
        self.logger.info("Version: %s", Globals.VERSION)
        self.logger.info("Build:   %d", Globals.BUILD)
        self.logger.info("-----------------------------------------------")

    def _outro(self):
        self.logger.info("Stopped")

    def _trigger(self):
        return

    def _start_cycler(self, config):
        freq = config["freq"]
        self.cycler = Cycler(freq, self._trigger)
        self.cycler.start()

    def _stop_cycler(self):
        self.cycler.stop()

    def _run(self):
        config = Config.load()

        self._start_cycler(config["cycler"])

        # Dummy 30 seconds execution
        event = threading.Event()
        event.wait(30)
        event.set()

        self._stop_cycler()

    def run(self):
        try:
            self._intro()
            self._run()
        except Exception as ex:
            self.logger.error(ex.message)
        finally:
            self._outro()
