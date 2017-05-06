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
            Spotter.KEY_NAME: self._name_filter,
            Spotter.KEY_EXE: self._exe_filter,
            Spotter.KEY_CMDLINE: self._cmdline_filter,
            Spotter.KEY_CWD: self._cwd_filter,
            Spotter.KEY_USERNAME: self._username_filter
        }

        self.active_filters = [self.supported_filters[key]
                               for key in self.config
                               if key in self.supported_filters]
        self.logger.info("Filters: %s", self.active_filters)

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _name_filter(self, proc):
        return proc.name() == self.config[Spotter.KEY_NAME]

    def _exe_filter(self, proc):
        return proc.exe() == self.config[Spotter.KEY_EXE]

    def _cmdline_filter(self, proc):
        return proc.cmdline() == self.config[Spotter.KEY_CMDLINE]

    def _cwd_filter(self, proc):
        return proc.cwd() == self.config[Spotter.KEY_CWD]

    def _username_filter(self, proc):
        return proc.username() == self.config[Spotter.KEY_USERNAME]

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

