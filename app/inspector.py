"""
Defines the Inspector class
"""

import logging
import threading
import Queue

from app.spotter import Spotter

from app.mem_probe import MemoryProbe
from app.cpu_probe import CpuProbe

class Inspector(threading.Thread):
    """
    A class that receives inspection & handling requests
    It can spot running processes that are of interest to us
    and inspect various aspects of them
    When required, it passes on the appropriate handling requests
    to the configured handler
    """

    KEY_TARGET = "target"
    KEY_RUNNING = "running"
    KEY_MEMORY = "memory"
    KEY_CPU = "cpu"

    KEY_CHECK = "check"
    KEY_TARGET = "target"
    KEY_REACTION = "reaction"

    def __init__(self, config, handler):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)

        self._configure(config) # Must come first after logger init

        self._init_probes()

        self.checks = {
            Inspector.KEY_RUNNING: self._check_running,
            Inspector.KEY_MEMORY: self._check_memory,
            Inspector.KEY_CPU: self._check_cpu
        }

        self.handler = handler
        self.queue = Queue.Queue()
        self.stopped = False

    def _init_probes(self):
        self.spotter = Spotter(self.config[Inspector.KEY_TARGET])

        if Inspector.KEY_MEMORY in self.config:
            self.mem_probe = MemoryProbe(self.config[Inspector.KEY_MEMORY])

        if Inspector.KEY_CPU in self.config:
            self.cpu_probe = CpuProbe(self.config[Inspector.KEY_CPU])

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            # Save original config
            self.config = config
        except KeyError as err:
            raise RuntimeError("Bad {0} configuration: {1}".format(__name__, err))

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _check_running(self, target):
        return target is not None

    def _check_memory(self, target):
        if not self.mem_probe:
            self.logger.error("Memory check aborted, probe not configured!")
            return True

        return self.mem_probe.valid(target)

    def _check_cpu(self, target):
        if not self.cpu_probe:
            self.logger.error("CPU check aborted, probe not configured!")
            return True

        return self.cpu_probe.valid(target)

    def _handle_target(self, target, reaction):
        self.handler.enqueue({
            Inspector.KEY_TARGET: target,
            Inspector.KEY_REACTION: reaction
        })

    def _process_target(self, target, request):
        if target is None:
            self.logger.info("Processing an inactive target")
        else:
            self.logger.info("Processting target [%s] pid [%d]", target.name(), target.pid)

        action_required = False

        reaction = request[Inspector.KEY_REACTION]
        for check in request[Inspector.KEY_CHECK]:
            self.logger.info("Processing request: %s -> %s", check, reaction)
            if not self.checks[check](target):
                self.logger.info("Check [%s] failed, action required!", check)
                action_required = True
                break

        if action_required:
            self._handle_target(target, reaction)

    def _process(self, request):
        targets = self.spotter.get_targets()
        # Target not running, push fake value to allow the running test to handle it
        if not targets:
            targets.append(None)

        # For each target, process request
        for target in targets:
            self._process_target(target, request)

    def enqueue(self, request):
        """
        Add an investigation request
        """
        self.queue.put(request)

    def stop(self):
        """
        Stop the investigator
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
