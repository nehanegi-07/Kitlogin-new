"""
Created on Jan 25th 2023

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2023 AnalyticKit, Inc"

"""

import os.path
import time
from datetime import datetime
from sca.datapipe.pipeline import Pipeline




def test_datapipe():
    # create python code to print timestamp since epoch
    timestamp = time.time()
    dt_object = datetime.fromtimestamp(timestamp)
    comp_name = dt_object.strftime("%Y-%m-%d_%H-%M-%S")
    hex_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    print("path=", os.getcwd())
    path = f"{os.getcwd()}/sca/resource/sca_config.ini"
    pipeline = Pipeline(comp_name, path, hex_address)
    pipeline.start(force_get=True)
