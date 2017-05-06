import logging
import threading
import subprocess
import Queue

class Handler(threading.Thread):

    def __init__(self, target, config):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.queue = Queue.Queue()
        self.stopped = False
        self.target = target
        self.config = config
        self.handlers = {
            "stop": self._target_stop,
            "start": self._target_start,
            "restart": self._target_restart
        }

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _target_stop(self, target):
        if "stop" in self.config:
            stop_config = self.config["stop"]
            cmd = stop_config["cmd"]
            args = ""
            if "args" in stop_config:
                args = stop_config["args"]
            subprocess.Popen([cmd, args])
        else:
            target.terminate()
            target.wait(timeout=3)

        self.logger.info("Stop issued!")

    def _target_start(self, target):
        if "start" in self.config:
            config = self.config["start"]
            cmd = config["cmd"]
        else:
            config = self.target
            cmd = self.target["name"]

        args = ""
        if "args" in config:
            args = config["args"]
        subprocess.Popen([cmd, args])
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
