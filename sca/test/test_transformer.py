# -*- coding: utf-8 -*-
"""
Created on June 6th 2022

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit, Inc"

"""
import pytest
import pathlib
import pandas as pd
import json
import re


from sca.transformer.trans import Transformer
from sca.common.config import ConfigHolder
from sca.common.storage import LocalStore
from sca.common.constants import TEST_DATA_DIR, CONFIG_DIR


@pytest.fixture()
def transformer():
    # os.getcwd() brings the root dir
    config = ConfigHolder(f"{CONFIG_DIR}sca_config.ini")
    store = LocalStore(config, "kitInc")

    return Transformer(config, store)


def test_transform(transformer):

    txn = transformer.transform_txns("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    int_txn = transformer.transform_internal_txns("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    log = transformer.transform_logs("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    contract_tok_info = transformer.transform_contract_tok_info("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    first_txn = transformer.transform_first_txn("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    erc20_add = transformer.transform_erc20_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    erc721_add = transformer.transform_erc721_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    erc20_con = transformer.transform_erc20_contract("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    erc721_con = transformer.transform_erc721_contract("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")

