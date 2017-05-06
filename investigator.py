import logging
import threading
import Queue

class Investigator(threading.Thread):

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.cond = threading.Condition()
        self.queue = Queue.Queue()
        self.config = config
        self.stopped = False

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def _process(self, request):
        self.logger.info("Processing request: %s", request)

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
