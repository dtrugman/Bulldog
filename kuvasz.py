#!/usr/bin/python

"""Kuvasz

Usage:
    kuvasz (service|app) <config-path>
    kuvasz (-h | --help)
    kuvasz --version

Options:
    -h --help       Show this screen
    --version       Show version
"""

import docopt

from app.version import Version
from app.runner import Runner

if __name__ == "__main__":
    VERSION = 'Kuvasz ' + Version.VERSION + '.' + Version.BUILD
    ARGS = docopt.docopt(__doc__, version=VERSION)
    SERVICE = ARGS['service'] # Boolean
    CONFIG_PATH = ARGS['<config-path>'] # String
    Runner.run(SERVICE, CONFIG_PATH)
