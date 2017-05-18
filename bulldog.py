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

import docopt

from app.version import Version
from app.runner import Runner

if __name__ == "__main__":
    VERSION = 'Bulldog ' + Version.VERSION + '.' + Version.BUILD
    ARGS = docopt.docopt(__doc__, version=VERSION)
    SERVICE = ARGS['service'] # Boolean
    CONFIG_PATH = ARGS['<config-path>'] # String
    Runner.run(SERVICE, CONFIG_PATH)
