"""
Defines the RestService class
"""

import web
import logging

class RestService(object):
    """
    A simple REST-ful web service
    Allows network triggers of checks and actions
    """

    KEY_IP = "ip"
    KEY_PORT = "port"

    '''URLS = (
        '/check/(.+)', check,
        '/react/(.+)', react
    )'''

    def __init__(self, target_name, config, investigator):
        self.target_name = target_name
        self.logger = logging.getLogger(self.target_name)

        self._configure(config) # Must come first after logger init

        self.investigator = investigator

        self._init_service()

    def _init_service(self):
        pass

    def _configure(self, config):
        """
        Reads and validates configuration
        """
        try:
            # Save original config
            self.config = config

            # Get configured ip
            self.ip = self.config[RestService.KEY_IP]

            # Get configured port
            # Allow both strings and numbers by using a cast here
            self.port = str(self.config[RestService.KEY_PORT])

            self.logger.info("Config: IP[%s] Port[%s]", self.ip, self.port)
        except (KeyError, TypeError) as err:
            raise RuntimeError("Bad {0} configuration: {1}".format(__name__, err))

    def _intro(self):
        self.logger.info("Starting")

    def _outro(self):
        self.logger.info("Stopped")

    def stop(self):
        """
        Stop the service
        """
        self._outro()

    def start(self):
        """
        Start the service
        """
        self._intro()
