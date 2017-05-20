"""
Defines the WinService class
"""

class WinService(object):
    """
    Win service wrapper
    """

    @staticmethod
    def start(config):
        """
        Start the service
        """
        print "Starting " + config
