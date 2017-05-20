"""
Defines the CpuProbe class
"""

import logging

class CpuProbe(object):
    """
    Probes the CPU usage of a target process and decides
    whether it has exceeded its configured limits or not
    """

    KEY_THRESHOLD = "threshold"
    KEY_PERIOD = "period"

    DEFAULT_THRESHOLD = 95 # 95% of a all CPUs
    DEFAULT_PERIOD = 4 # To avoid common CPU peaks

    def __init__(self, target_name, config):
        self.target_name = target_name
        self.logger = logging.getLogger(self.target_name)

        self._configure(config) # Must come first after logger init

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            # Save original config
            self.config = config

            self.threshold = self.config.get(CpuProbe.KEY_THRESHOLD,
                                             CpuProbe.DEFAULT_THRESHOLD)

            self.period = self.config.get(CpuProbe.KEY_PERIOD,
                                          CpuProbe.DEFAULT_PERIOD)

            self.logger.info("Config: Threshold[%d] Period[%d]",
                             self.threshold, self.period)
        except KeyError as err:
            raise RuntimeError("Bad {0} configuration: {1}".format(__name__, err))

    def _sample_cpu(self, target):
        """
        Read the CPU usage of the target
        """
        return target.cpu_percent(interval=1)

    def valid(self, target):
        """
        Probe the target's current CPU usage
        Returns True if the target's CPU is withing limits or not active(!)
        """
        self.logger.debug("Probing target CPU usage")
        if target is None:
            self.logger.debug("Target not running, skipping")
            return True

        # Always sample once(!)
        # Number of samples is 'self.period + 1'
        total = self._sample_cpu(target)

        for _ in xrange(self.period):
            total += self._sample_cpu(target)
            # The cpu_percent call creates the interval

        # Calculate avarage CPU usage
        samples = self.period + 1
        avg = total / samples
        self.logger.info("Sampled %d times, %d percent on average, threshold is %d",
                         samples, avg, self.threshold)

        # Return true if target exceeded
        return avg <= self.threshold
