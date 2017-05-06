"""
Defines the Handler class
"""

import logging
import threading
import subprocess
import Queue

class Handler(threading.Thread):
    """
    A handler class that can stop/start/restart
    the target process
    """

    KEY_STOP = "stop"
    KEY_START = "start"

    KEY_CMD = "cmd"
    KEY_ARGS = "args"

    CMD_LINE_ITEM = [KEY_CMD, KEY_ARGS]

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)

        self._configure(config) # Must come first after logger init

        self.queue = Queue.Queue()
        self.stopped = False

        self.handlers = {
            "stop": self._target_stop,
            "start": self._target_start,
            "restart": self._target_restart
        }

    def _cmdline_config_parser(self, key, value):
        if len(value) != len(Handler.CMD_LINE_ITEM):
            raise KeyError("Command line item[{0}] misconfigured".format(key))

        for item in value:
            if item not in Handler.CMD_LINE_ITEM:
                raise KeyError("Command line item[{0}] bad key[{1}]".format(key, item))

        if not isinstance(value[Handler.KEY_CMD], basestring):
            raise KeyError("Command line item[{0}] bad key[{1}] value: "
                           "non-string".format(key, Handler.KEY_CMD))

        if not isinstance(value[Handler.KEY_ARGS], list):
            raise KeyError("Command line item[{0}] bad key[{1}] value: "
                           "not a list".format(key, Handler.KEY_ARGS))

        for item in value[Handler.KEY_ARGS]:
            if not isinstance(item, basestring):
                raise KeyError("Command line item[{0}] bad key[{1}] value: "
                               "contains non-string".format(key, Handler.KEY_ARGS))

        cmdline = [value[Handler.KEY_CMD]]
        cmdline += value[Handler.KEY_ARGS]
        return cmdline

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            self.logger.info("Configuration:")

            # Save original config
            self.config = config

            # Get configured stop action
            # If none specified, we will use the default termination
            # functionality of psutil
            self.stop_cmd = []
            if Handler.KEY_STOP in self.config:
                self.stop_cmd = self._cmdline_config_parser(Handler.KEY_STOP,
                                                            self.config[Handler.KEY_STOP])
            self.logger.info("Stop cmdline: %s", self.stop_cmd)

            self.start_cmd = self._cmdline_config_parser(Handler.KEY_START,
                                                         self.config[Handler.KEY_START])
            self.logger.info("Start cmdline: %s", self.start_cmd)
        except KeyError as err:
            raise RuntimeError("Bad {0} configuration: {1}".format(__name__, err))

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _target_stop(self, target):
        if target is None:
            self.logger.info("Stop skipped, target not active")
            return

        if self.stop:
            subprocess.Popen(self.stop_cmd)
        else:
            target.terminate().wait(timeout=3)

        self.logger.info("Stop issued!")

    def _target_start(self, target):
        subprocess.Popen(self.start_cmd)
        self.logger.info("Start issued!")

    def _target_restart(self, target):
        self._target_stop(target)
        self._target_start(target)

    def _process(self, request):
        target = request["target"]
        react = request["react"]
        for reaction in react:
            if target is None:
                self.logger.info("Handling an inactive target -> Executing %s",
                                 reaction)
            else:
                self.logger.info("Handling target [%s] pid [%d] -> Executing %s",
                                 target.name(), target.pid, reaction)
            self.handlers[reaction](target)

    def enqueue(self, request):
        """
        Add a handling request
        """
        self.queue.put(request)

    def stop(self):
        """
        Stop the handler
        """
        self.stopped = True
        # Insert fake item to ensure we exit the blocking the get()
        self.queue.put("*")

    def run(self):
        self._intro()
        while True:
            request = self.queue.get()
            if self.stopped:
                break
            self._process(request)
        self._outro()
