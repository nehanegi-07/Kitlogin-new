"""
Created on May 4th 2022

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""


import configparser
import logging

class ConfigHolder:
    """
    This class reads configuration values from sca_config.ini file
    """

    section_names = "kafka_server", "kafka_topic", "aws_dynamoDB", \
        "aws_secrets", "logging", "gcp", "ether_scan", "storage", \
        "ethplorer", "eta", "archivenode"

    def __init__(self, *file_names):
        '''
        Initialize ConfigHolder object

        Parameters
        ----------
        *file_names : str
            Name of configuration file names

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        logger = logging.getLogger(__name__)
        parser = configparser.ConfigParser()
        parser.optionxform = str  # make option names case sensitive
        found = parser.read(file_names)
        if not found:
            logger.error('No config file found:%s' %file_names)
            raise ValueError('No config file found:%s' %file_names)
        for name in ConfigHolder.section_names:
            self.__dict__.update(parser.items(name))

    def get_value(self, key):
        '''
        Return value for the given key

        Parameters
        ----------
        key : str
            key to retrieve the value

        Returns
        -------
        TYPE
            Value associated withe the key.

        '''

        return self.__dict__.get(key)

    def set_value(self, key, value):
        '''
        Set value for the given key. This function is used to change the
        default conig key-value pair. Primarily used for functional test
        to load specific values.

        Parameters
        ----------
        key : str
            key to set the value
        value : str
            value to set

        Returns
        -------
        None.

        '''

        self.__dict__[key] = value
