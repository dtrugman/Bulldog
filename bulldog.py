#!/usr/bin/python

"""Bulldog

Usage:
    Bulldog (service|app) <config-path>
    Bulldog (-h | --help)
    Bulldog --version

Options:
    -h --help       Show this screen
    --version       Show version
"""

import os
import sys
import docopt

from app.version import Version
from app.runner import Runner

def getcwd():
    """
    Gets the real path to the executable's dir
    """
    # If this is an executable created by pyinstaller
    # get path from the system executable
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    # If this is a regular file, get it's path
    if __file__:
        return os.path.dirname(__file__)

    print "Cannot detect current working directory"
    sys.exit(1)

if __name__ == "__main__":
    # Parse arguments
    VERSION = 'Bulldog ' + Version.VERSION + '.' + Version.BUILD
    ARGS = docopt.docopt(__doc__, version=VERSION)
    SERVICE = ARGS['service'] # Boolean
    CONFIG_PATH = ARGS['<config-path>'] # String

    # Set cwd
    CWD = getcwd()
    os.chdir(CWD)

    # Run
    Runner.run(SERVICE, CONFIG_PATH)
