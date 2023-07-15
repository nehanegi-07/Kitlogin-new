# -*- coding: utf-8 -*-
"""
Created on May 4th 2022

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit, Inc"

"""
import pytest
import os.path

from sca.common.config import ConfigHolder


@pytest.fixture()
def load_config():
    path = os.getcwd()+"/sca/resource/"
    print("path=",path)
    return ConfigHolder(path+"sca_config.ini")


def test_getValue(load_config):
    assert load_config.get_value("auto_offset_reset") == "latest"
    assert load_config.get_value("log_level") == "debug"

