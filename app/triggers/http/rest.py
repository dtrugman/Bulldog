"""
Defines the RestService and RestApplication classes
"""

import threading
import logging
import web

class check(object):
    """
    Handles GET requests to the 'check' API
    """
    def GET(self, check):
        """
        Handle GET request
        """
        print "GET"
        print check
        return "get"

class react(object):
    """
    Handles POST requests to the 'react' API
    """
    def POST(self):
        """
        Handle POST request
        """
        args = web.input()
        print "POST"
        raise web.seeother('/')

class RestLogger(object):
    """
    A wrapper for the loggings library
    Wraps exactly ONE logging method, e.g. logger.info or logger.debug
    """
    def __init__(self, log_method):
        self.log_method = log_method

    def write(self, data):
        """
        Write to log
        """
        if data:
            data = data.strip()

        if not data:
            return

        if data[-1:] == '\n':
            data = data[:-1]

        self.log_method(data)


class RestApplication(web.application):
    """
    A wrapper for the web.py application
    Allows us to use custom configuration
    """
    def run(self, ip, port, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (ip, port))

    def stop(self):
        web.httpserver.server.stop()
        web.httpserver.server = None

class RestService(threading.Thread):
    """
    A simple REST-ful web service
    Allows network triggers of checks and actions
    """

    KEY_IP = "ip"
    KEY_PORT = "port"

    URLS = (
        '/check/(.+)', 'check',
        '/react/(.+)', 'react'
    )

    def __init__(self, target_name, config, investigator):
        threading.Thread.__init__(self)

        self.target_name = target_name
        self.logger = logging.getLogger(self.target_name)
        self.stdout_wrapper = RestLogger(self.logger.info)
        self.stderr_wrapper = RestLogger(self.logger.warning)

        self._configure(config) # Must come first after logger init

        self.investigator = investigator

        self._init_service()

    def _init_service(self):
        try:
            web.httpserver.sys.stdout = self.stdout_wrapper
            web.httpserver.sys.stderr = self.stderr_wrapper

            self.app = RestApplication(RestService.URLS, globals())
        except Exception as err:
            self.logger.error(err)

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
            self.port = int(self.config[RestService.KEY_PORT])

            self.logger.info("Config: IP[%s] Port[%d]", self.ip, self.port)
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
        if self.app:
            self.app.stop()

    def run(self):
        self._intro()
        self.app.run(self.ip, self.port)
