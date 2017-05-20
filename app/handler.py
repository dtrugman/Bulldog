"""
Defines the Handler class
"""

import logging
import psutil

from app.globals import Globals

class Handler(object):
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

    def __init__(self, target_name, config):
        self.target_name = target_name
        self.logger = logging.getLogger(self.target_name)

        self._init_default_handlers()
        self._configure(config)

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
            # Save original config
            self.config = config

            # Read configured actions
            for key, value in self.config.iteritems():
                cmdline = self._parse_cmdline(value)
                self.handlers[key] = (self._target_action, cmdline)
                self.logger.info("Added command[%s]: %s", key, cmdline)
        except KeyError as err:
            raise RuntimeError("Bad {0} configuration: {1}".format(__name__, err))

    def _target_stop(self, target, args):
        if target is None:
            self.logger.info("Stop skipped, target not active")
            return

        try:
            target.terminate()
            self.logger.warning("Stop issued!")
            target.wait(timeout=Globals.KILL_WAIT_TIMEOUT)
            self.logger.warning("Stop target successful!")
        except psutil.TimeoutExpired:
            self.logger.error("Stop target failed!")

    def _target_action(self, target, args):
        try:
            self.logger.warning("Issued command [%s]", args)
            psutil.Popen(args)
        except (OSError, ValueError) as err:
            self.logger.error("Command failed! err: %s", err)

    def process(self, request):
        """
        Process a handling request
        """
        target = request[Handler.KEY_TARGET]
        if target is None:
            self.logger.debug("Handling an inactive target")
        else:
            self.logger.debug("Handling target [%s] pid [%d]", target.name(), target.pid)

        reaction = request[Handler.KEY_REACTION]
        for action in reaction:
            self.logger.warning("Executing %s", action)
            if action not in self.handlers:
                self.logger.error("Action %s aborted, action not configured!", action)
                continue

            handler, args = self.handlers[action] # Get registered handler and args
            handler(target, args) # Execute handler while passing target and args
