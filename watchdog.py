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
        self.cycler_conf = None

        self.investigator = None
        self.investigator_conf = None

    def _intro(self):
        self.logger.info("-----------------------------------------------")
        self.logger.info("Starting")
        self.logger.info("-----------------------------------------------")
        self.logger.info("Version: %s", Globals.VERSION)
        self.logger.info("Build:   %d", Globals.BUILD)
        self.logger.info("-----------------------------------------------")

    def _outro(self):
        self.logger.info("Stopped")

    def _cycler_trigger(self):
        manifest = self.cycler_conf["manifest"]
        for item in manifest:
            for check in item["check"]:
                self.logger.info("Investigating %s", check)

    def _cycler_start(self, config):
        # TODO: Check config contains what we expect
        self.cycler_conf = config
        self.cycler = Cycler(self.cycler_conf["freq"], self._cycler_trigger)
        self.cycler.start()

    def _cycler_stop(self):
        self.cycler.stop()

    def _investigator_start(self, config):
        # TODO: Check config contains what we expect
        self.investigator_conf = config
        self.investigator = Investigator(config)
        self.investigator.start()

    def _investigator_stop(self):
        self.investigator.stop()

    def _run(self):
        config = Config.load()
        self._investigator_start(config["investigator"])
        self._cycler_start(config["cycler"])

    def _stop(self):
        self._cycler_stop()
        self._investigator_stop()

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
