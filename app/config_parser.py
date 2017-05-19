"""
Defines the Config Parser class
"""
import json
import os

class ConfigParser(object):
    """
    A class that is responsible for loading configuration
    """

    KEY_LOG = "log"
    KEY_WATCHDOGS = "watchdogs"

    KEY_DIR = "dir"
    KEY_LEVEL = "level"

    LOG_SECTIONS = [KEY_DIR, KEY_LEVEL]

    @staticmethod
    def _check_section(config, name, sections):
        section_config = config[name]
        for section in sections:
            if section not in section_config:
                raise RuntimeError("Bad config, missing {0} section[{1}]".format(name, section))

    @staticmethod
    def _check(config):
        if not config:
            raise RuntimeError("Empty config")

        # Check log section

        if ConfigParser.KEY_LOG not in config:
            raise RuntimeError("Bad config, missing section[{0}]".format(ConfigParser.KEY_LOG))

        ConfigParser._check_section(config, ConfigParser.KEY_LOG, ConfigParser.LOG_SECTIONS)

        # Check watchdogs section

        if ConfigParser.KEY_WATCHDOGS not in config:
            raise RuntimeError("Bad config, missing section[{0}]".format(ConfigParser.KEY_LOG))

    @staticmethod
    def load(path):
        """
        Loads the configuration file specified by the command line arguments
        """
        if not os.path.isfile(path):
            raise RuntimeError("Bad config file path[{0}]".format(path))

        config = {}
        with open(path) as jfile:
            config = json.load(jfile)

        # Throws RuntimeError if not valid
        ConfigParser._check(config)

        return config
