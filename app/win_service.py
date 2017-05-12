"""
Defines the WinService class
"""

import logging

class WinService(object):
    """
    Win service wrapper
    """

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config

    def start(self):
        self.logger.info("Starting")