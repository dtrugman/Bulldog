"""
Defines the WinService class
"""

class WinService(object):
    """
    Win service wrapper
    """

    @staticmethod
    def start(config_path):
        """
        Start the service
        """
        print "Starting " + config_path
