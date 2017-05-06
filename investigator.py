import psutil
import logging
import threading
import Queue

class Investigator(threading.Thread):

    def __init__(self, target, config):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.queue = Queue.Queue()
        self.target = target
        self.config = config
        self.stopped = False
        self.checks = {
            "running": self._check_running,
            "memory": self._check_memory,
            "cpu": self._check_cpu
        }

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _get_running_targets(self):
        """
        Returns an array of psutil handles to target processes
        The array will be empty if the target is not running
        """
        target_name = self.target["name"]
        return [proc for proc in psutil.process_iter() if proc.name() == target_name]

    def _check_running(self, target):
        """
        Check if the target process is running
        Return value says if check requires a reaction
        """
        self.logger.info("Checking target is running")
        return target is None

    def _check_memory(self, target):
        """
        Check if the target process has exceeded its
        memory thrashold
        Return value says if check requires a reaction
        """
        self.logger.info("Checking target memory usage")
        if target is None:
            self.logger.info("Target not running, skipping")
            return False

        mem = target.memory_full_info() # Linux/OSX/Win only
        threshold = self.config["memory"]["threshold"]
        self.logger.info("Target memory[%d] threshold[%d]", mem.uss, threshold)
        return mem.uss > threshold

    def _check_cpu(self, target):
        """
        Check if the target process has exceeded its
        cpu thrashold
        Return value says if check requires a reaction
        """
        self.logger.info("Checking target cpu usage")
        if target is None:
            self.logger.info("Target not running, skipping")
            return False

        cpu = target.cpu_percent(interval=1)
        threshold = self.config["cpu"]["threshold"]
        self.logger.info("Target cpu[%d] threshold[%d]", cpu, threshold)
        return cpu > threshold

    def _process_target(self, target, request):
        if target is None:
            self.logger.info("Processing an inactive target")
        else:
            self.logger.info("Processting target [%s] pid [%d]", target.name(), target.pid)

        react = request["react"]
        for check in request["check"]:
            self.logger.info("Processing request: %s -> %s", check, react)
            action_required = self.checks[check](target)
            self.logger.info("Check [%s] action required? %s", check, action_required)
            if action_required:
                pass

    def _process(self, request):
        # We assume every request needs to know the process' pid
        # so we always get it here
        targets = self._get_running_targets()
        # Target not running, push fake value to allow the running test to handle it
        if not targets:
            targets.append(None)

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
