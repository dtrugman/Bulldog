"""
Defines the Spotter class
"""

import logging
import psutil

class Spotter(object):
    """
    A class for spotting target processes
    """

    KEY_NAME = "name"
    KEY_EXE = "exe"
    KEY_CMDLINE = "cmdline"
    KEY_CWD = "cwd"
    KEY_USERNAME = "username"

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)

        self._configure(config) # Must come first after logger init
        self._compile_filters()

        self.errors_history = {}

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            self.logger.info("Configuration:")

            # Save original config
            self.config = config
            self.logger.info("Target: %s", self.config)
        except KeyError as err:
            raise RuntimeError("Bad Spotter configuration: " + str(err))

    def _compile_filters(self):
        self.supported_filters = {
            Spotter.KEY_NAME: lambda proc: proc.name() == self.config[Spotter.KEY_NAME],
            Spotter.KEY_EXE: lambda proc: proc.exe() == self.config[Spotter.KEY_EXE],
            Spotter.KEY_CMDLINE: lambda proc: proc.cmdline() == self.config[Spotter.KEY_CMDLINE],
            Spotter.KEY_CWD: lambda proc: proc.cwd() == self.config[Spotter.KEY_CWD],
            Spotter.KEY_USERNAME: lambda proc: proc.username() == self.config[Spotter.KEY_USERNAME]
        }

        requested_filters = [key for key in self.config
                             if key in self.supported_filters]
        self.logger.info("Filters: %s", requested_filters)

        self.active_filters = [self.supported_filters[key]
                               for key in requested_filters]
        # We don't use beautiful one-line comprehension so we could log the active filter

    def _filter(self, proc):
        try:
            for proc_filter in self.active_filters:
                if not proc_filter(proc):
                    return False
            return True
        except psutil.AccessDenied:
            if proc.pid not in self.errors_history or proc.name() != self.errors_history[proc.pid]:
                self.errors_history[proc.pid] = proc.name()
                self.logger.info("Cannot check process[%s] pid[%d]", proc.name(), proc.pid)

    def get_targets(self):
        """
        Get all running target processes
        """
        return [proc for proc in psutil.process_iter() if self._filter(proc)]

