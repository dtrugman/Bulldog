"""
Defines the MemoryProbe class
"""

import logging
import time

class MemoryProbe(object):
    """
    Probes the memory usage of a target process and decides
    whether it has exceeded its configured limits or not
    """

    KEY_THRESHOLD = "threshold"
    KEY_PERIOD = "period"
    KEY_SET = "set"

    DEFAULT_THRESHOLD = 500000000 # 500MB
    DEFAULT_PERIOD = 0 # Single sample
    DEFAULT_SET = "uss" # Considered the most reliable metric

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)

        self._configure(config) # Must come first after logger init

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            self.logger.info("Configuration:")

            # Save original config
            self.config = config

            self.threshold = self.config.get(MemoryProbe.KEY_THRESHOLD,
                                             MemoryProbe.DEFAULT_THRESHOLD)
            self.logger.info("Threshold: %d", self.threshold)

            self.period = self.config.get(MemoryProbe.KEY_PERIOD,
                                          MemoryProbe.DEFAULT_PERIOD)
            self.logger.info("Period: %d", self.period)

            self.set = self.config.get(MemoryProbe.KEY_SET,
                                       MemoryProbe.DEFAULT_SET)
            self.samplers = {
                "rss": lambda mem: mem.rss,
                "vms": lambda mem: mem.vms,
                "uss": lambda mem: mem.uss,
                "pss": lambda mem: mem.pss
            }
            self.sampler = self.samplers.get(self.set)
            if self.sampler is None:
                raise KeyError("Bad memory set[{0}]".format(self.set))
            self.logger.info("Set: %s", self.set)
        except KeyError as err:
            raise RuntimeError("Bad {0} configuration: {1}".format(__name__, err))

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _sample_rss(self, target_memory):
        return target_memory.uss

    def _sample_memory(self, target):
        """
        Read the memory usage of the target
        """
        return self.sampler(target.memory_full_info())

    def valid(self, target):
        """
        Probe the target's current memory usage
        Returns True if the target's memory is withing limits or not active(!)
        """
        self.logger.info("Probing target memory usage")
        if target is None:
            self.logger.info("Target not running, skipping")
            return True

        # Always sample once(!)
        # Number of samples is 'self.period + 1'
        total = self._sample_memory(target)

        for _ in xrange(self.period):
            total += self._sample_memory(target)
            time.sleep(1)

        # Calculate avarage memory usage
        samples = self.period + 1
        avg = total / samples
        self.logger.info("Sampled %d times, %d bytes on average, threshold is %d",
                         samples, avg, self.threshold)

        # Return true if target exceeded
        return avg <= self.threshold
