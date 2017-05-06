import logging
import threading
import Queue

class Handler(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.queue = Queue.Queue()
        self.stopped = False
        self.handlers = {
            "stop": self._target_stop,
            "start": self._target_start,
            "restart": self._target_restart
        }

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _target_stop(self):
        pass

    def _target_start(self):
        pass

    def _target_restart(self):
        self._target_stop()
        self._target_start()

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
