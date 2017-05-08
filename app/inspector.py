import logging
import threading
import Queue

from spotter import Spotter

from mem_probe import MemoryProbe
from cpu_probe import CpuProbe

class Inspector(threading.Thread):

    KEY_TARGET = "target"
    KEY_MEMORY = "memory"
    KEY_CPU = "cpu"

    def __init__(self, config, handler):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)

        self._configure(config) # Must come first after logger init

        self.queue = Queue.Queue()
        self.stopped = False

        self.spotter = Spotter(self.config[Inspector.KEY_TARGET])
        self.mem_probe = MemoryProbe(self.config[Inspector.KEY_MEMORY])
        self.cpu_probe = CpuProbe(self.config[Inspector.KEY_CPU])

        self.handler = handler
        self.checks = {
            "running": self._check_running,
            "memory": self._check_memory,
            "cpu": self._check_cpu
        }

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            self.logger.info("Configuration:")

            # Save original config
            self.config = config
        except KeyError as err:
            raise RuntimeError("Bad {0} configuration: {1}".format(__name__, err))

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _check_running(self, target):
        """
        Check if the target process is running
        Return value says if check requires a reaction
        """
        self.logger.info("Checking target is running")
        return target is not None

    def _check_memory(self, target):
        """
        Check if the target process has exceeded its
        memory thrashold
        Return value says if check requires a reaction
        """
        return self.mem_probe.valid(target)

    def _check_cpu(self, target):
        """
        Check if the target process has exceeded its
        cpu thrashold
        Return value says if check requires a reaction
        """
        return self.cpu_probe.valid(target)

    def _process_target(self, target, request):
        if target is None:
            self.logger.info("Processing an inactive target")
        else:
            self.logger.info("Processting target [%s] pid [%d]", target.name(), target.pid)

        action_required = False

        react = request["react"]
        for check in request["check"]:
            self.logger.info("Processing request: %s -> %s", check, react)
            if not self.checks[check](target):
                self.logger.info("Check [%s] failed, action required!", check)
                action_required = True
                break

        if action_required:
            handler_request = {
                "target": target,
                "react": react
            }
            self.handler.enqueue(handler_request)

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
