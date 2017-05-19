"""
Defines the Globals class
"""

class Globals(object):
    """
    A class that is responsible for constant global values
    """

    APP_NAME = "bulldog"

    LOG_DIR = "/var/log/" + APP_NAME
    LOG_FILE = LOG_DIR + "/" + APP_NAME + ".log"
    LOG_TERM = LOG_DIR + "/" + APP_NAME + ".term"
    LOG_FORMAT = "%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s"

    PID_DIR = "/var/run"
    PID_FILE = PID_DIR + "/" + APP_NAME + ".pid"
    PID_ACQUIRE_TIMEOUT = 1

    KILL_WAIT_TIMEOUT = 3
