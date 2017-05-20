"""
Defines the Cycler class
"""

import logging

from app.triggers.time.periodic_timer import PeriodicTimer

class Cycler(object):
    """
    A simple object that uses a periodic timer and
    pushes investigation requests each time it's triggered
    """

    KEY_FREQ = "freq"
    KEY_MANIFEST = "manifest"
    KEY_CHECK = "check"
    KEY_REACT = "reaction"

    MANIFEST_ITEM = [KEY_CHECK, KEY_REACT]

    def __init__(self, target_name, config, investigator):
        self.target_name = target_name
        self.logger = logging.getLogger(self.target_name)

        self._configure(config) # Must come first after logger init

        self.investigator = investigator
        self.periodic_timer = PeriodicTimer(self.target_name, self.freq, self._trigger)

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            # Save original config
            self.config = config

            # Get configured frequency
            # Allow both numbers and string by using a cast
            self.freq = int(self.config[Cycler.KEY_FREQ])

            # Get and check configured manifest
            # Rules:
            # Manifest is a dictionary
            # Each item in the dictionary is a item, which is also a dictionary
            # Each item has exactly the same keys as Cycler.KEY_MANIFEST
            # Each key's value is a list of strings
            self.manifest = self.config[Cycler.KEY_MANIFEST]
            for idx, item in enumerate(self.manifest):
                if len(item) != len(Cycler.MANIFEST_ITEM):
                    raise KeyError("Manifest item[{0}] misconfigured".format(idx))

                for key in item:
                    if key not in Cycler.MANIFEST_ITEM:
                        raise KeyError("Manifest item[{0}] bad key[{1}]".format(idx, key))

                    if not isinstance(item[key], list):
                        raise KeyError("Manifest item[{0}] bad key[{1}] value: "
                                       "not a list".format(idx, key))

                    for val in item[key]:
                        if not isinstance(val, basestring):
                            raise KeyError("Manifest item[{0}] bad key[{1}] value: "
                                           "contains non-string".format(idx, key))

            self.logger.info("Config: Freq[%d]s Manifest[%s]",
                             self.freq, self.manifest)
        except (KeyError, TypeError) as err:
            raise RuntimeError("Bad {0} configuration: {1}".format(__name__, err))

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _trigger(self):
        for item in self.manifest:
            self.logger.debug("Enqueuing request: %s", item)
            self.investigator.enqueue(item)

    def stop(self):
        """
        Stop the cycler
        """
        self.periodic_timer.stop()
        self._outro()

    def start(self):
        """
        Start the cycler.
        It will execute the specified action every 'freq' seconds
        """
        self._intro()
        self.periodic_timer.start()
