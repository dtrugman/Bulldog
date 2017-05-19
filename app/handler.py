"""
Defines the Handler class
"""

import logging
import threading
import subprocess
import psutil
import Queue

from app.globals import Globals

class Handler(threading.Thread):
    """
    A handler class that can stop/start/restart
    the target process
    """

    KEY_STOP = "stop"
    KEY_START = "start"
    KEY_RESTART = "restart"

    KEY_TARGET = "target"
    KEY_REACTION = "reaction"

    KEY_CMD = "cmd"
    KEY_ARGS = "args"

    CMD_LINE_ITEM = [KEY_CMD, KEY_ARGS]

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)

        self._init_default_handlers()
        self._configure(config)

        self.queue = Queue.Queue()
        self.stopped = False

    def _init_default_handlers(self):
        # The handlers map holds pairs: <function, arg>
        self.handlers = {}

        if Handler.KEY_START not in self.handlers:
            self.handlers[Handler.KEY_STOP] = (self._target_stop, None)

    def _parse_cmdline(self, value):
        """
        Parses a value that is expected to contain a complete command line
        """

        if len(value) != len(Handler.CMD_LINE_ITEM):
            raise KeyError("Command line item misconfigured")

        for item in value:
            if item not in Handler.CMD_LINE_ITEM:
                raise KeyError("Command line bad key[{0}]".format(item))

        if not isinstance(value[Handler.KEY_CMD], basestring):
            raise KeyError("Command line item bad key[{0}] value: "
                           "non-string".format(Handler.KEY_CMD))

        if not isinstance(value[Handler.KEY_ARGS], list):
            raise KeyError("Command line item bad key[{0}] value: "
                           "not a list".format(Handler.KEY_ARGS))

        for item in value[Handler.KEY_ARGS]:
            if not isinstance(item, basestring):
                raise KeyError("Command line item bad key[{0}] value: "
                               "contains non-string".format(Handler.KEY_ARGS))

        cmdline = [value[Handler.KEY_CMD]]
        if value[Handler.KEY_ARGS]:
            cmdline += value[Handler.KEY_ARGS]
        else:
            cmdline += [''] # We append an empty string to be compatible with psutil
        return cmdline

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            self.logger.info("Configuration:")

            # Save original config
            self.config = config

            # Read configured actions
            for key, value in self.config.iteritems():
                cmdline = self._parse_cmdline(value)
                self.handlers[key] = (self._target_action, cmdline)
                self.logger.info("Added command[%s]: %s", key, cmdline)
        except KeyError as err:
            raise RuntimeError("Bad {0} configuration: {1}".format(__name__, err))

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _target_stop(self, target, args):
        if target is None:
            self.logger.info("Stop skipped, target not active")
            return

        try:
            target.terminate()
            self.logger.info("Stop issued!")
            target.wait(timeout=Globals.KILL_WAIT_TIMEOUT)
            self.logger.info("Stop target successful!")
        except psutil.TimeoutExpired:
            self.logger.error("Stop target failed!")

    def _target_action(self, target, args):
        try:
            self.logger.info("Issued command [%s]", args)
            subprocess.Popen(args)
        except (OSError, ValueError) as err:
            self.logger.error("Command failed! err: %s", err)

    def _process(self, request):
        target = request[Handler.KEY_TARGET]
        reaction = request[Handler.KEY_REACTION]
        for action in reaction:
            if target is None:
                self.logger.info("Handling an inactive target -> Executing %s",
                                 action)
            else:
                self.logger.info("Handling target [%s] pid [%d] -> Executing %s",
                                 target.name(), target.pid, action)

            if action not in self.handlers:
                self.logger.error("Action %s aborted, action not configured!",
                                  action)
                continue

            handler, args = self.handlers[action] # Get registered handler and args
            handler(target, args) # Execute handler while passing target and args

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

            try:
                self._process(request)
            except OSError as err:
                self.logger.info("Handling failed: %s", err)
        self._outro()
