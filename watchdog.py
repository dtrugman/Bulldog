import logging

from config import Config
from config import Globals

class WatchDog:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s :: %(levelname)s :: %(message)s')
        self._logger = logging.getLogger('watchdog')
        self._logger.setLevel(logging.DEBUG)

    def _intro(self):
        self._logger.info("-----------------------------------------------")
        self._logger.info("WatchDog starting")
        self._logger.info("-----------------------------------------------")
        self._logger.info("Version: %s", Globals.VERSION)
        self._logger.info("Build:   %d", Globals.BUILD)
        self._logger.info("-----------------------------------------------")

    def _outro(self):
        self._logger.info("WatchDog stopped")

    def _run(self):
        config = Config.load()

    def run(self):
        try:
            self._intro()
            self._run()
        except Exception as ex:
            self._logger.error(ex.message)
        finally:
            self._outro()
