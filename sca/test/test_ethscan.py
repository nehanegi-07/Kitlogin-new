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

from sca.extractor.ethextract import EthExtractor
from sca.common.config import ConfigHolder
from sca.common.storage import LocalStore
from sca.common.constants import TEST_DATA_DIR, CONFIG_DIR


@pytest.fixture()
def eth_ext():
    # os.getcwd() brings the root dir
    config = ConfigHolder(f"{CONFIG_DIR}sca_config.ini")
    store = LocalStore(config, "kitInc")

    return EthExtractor(config, store)


def test_get_txns_by_address(eth_ext):
    rt_txns = eth_ext.get_txns_by_address(
        "0xd4f11C30078d352354c0B17eAA8076C825416493", force_get=True
    )
    assert rt_txns is not None
    assert type(rt_txns) is list
    assert len(rt_txns) > 0, "Transaction count is not greater thn 0"

    # get data from the json file for one record
    stored_txn_data = pathlib.Path(f"{TEST_DATA_DIR}/txns.json").read_text()

    assert rt_txns[0].get("blockNumber") == '14879161'

    # Convert JSON string with records orient to a Dataframe
    df = pd.read_json(stored_txn_data, orient='records')
    df = df.astype(str)

    # compare df stored JSON with real-time retrieved data from Etherscan
    assert df["blockNumber"].iloc[0] == rt_txns[0].get("blockNumber")
    assert df["hash"].iloc[0] == rt_txns[0].get("hash")
    assert df["blockHash"].iloc[0] == rt_txns[0].get("blockHash")
    assert df["value"].iloc[0] == rt_txns[0].get("value")
    assert df["gasPrice"].iloc[0] == rt_txns[0].get("gasPrice")
    assert df["transactionIndex"].iloc[0] == rt_txns[0].get("transactionIndex")
    assert df["txreceipt_status"].iloc[0] == rt_txns[0].get("txreceipt_status")
    assert df["txreceipt_status"].iloc[0] == rt_txns[0].get("txreceipt_status")


def test_get_contract_abi(eth_ext):
    rt_abi = eth_ext.get_contract_abi(
        "0xd4f11C30078d352354c0B17eAA8076C825416493", force_get=True)

    # get data from the json file
    f = open(f"{TEST_DATA_DIR}/abi.json")
    stored_abi_data = json.load(f)

    assert rt_abi is not None
    assert stored_abi_data is not None

    # convert realtime retrieved abi and stored abi to str, hash and compare the value
    assert hash(str(rt_abi)) == hash(str(stored_abi_data))


def test_get_total_token_supply_by_contract_address(eth_ext):
    rt_toekn_info = eth_ext.get_total_token_supply_by_contract_address(
        "0x57d90b64a1a57749b0f932f1a3395792e12e7055", force_get=True)

    # get data from the json file
    f = open(f"{TEST_DATA_DIR}/token_info.json")
    stored_toekn_info_data = json.load(f)

    assert rt_toekn_info is not None
    assert stored_toekn_info_data is not None

    # convert realtime retrieved abi and stored abi to str, hash and compare the value
    assert hash(str(rt_toekn_info)) == hash(str(stored_toekn_info_data))


def test_get_log_by_contract(eth_ext):
    rt_log = eth_ext.get_log_by_contract(
        "0x57d90b64a1a57749b0f932f1a3395792e12e7055", force_get=True)

    # get data from the json file
    f = open(f"{TEST_DATA_DIR}/log.json")
    stored_log_data = json.load(f)

    assert rt_log is not None
    assert stored_log_data is not None

    # convert realtime retrieved abi and stored abi to str, hash and compare the value
    assert hash(str(rt_log)) == hash(str(stored_log_data))


def test_get_erc20_token_transfer_events_by_address(eth_ext):
    rt_erc20_eoa = eth_ext.get_erc20_token_transfer_events_by_address(
        "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", force_get=True)

    # get data from the json file
    f = open(f"{TEST_DATA_DIR}/erc20_eoa.json")
    stored_erc20_eor_data = json.load(f)

    assert rt_erc20_eoa is not None
    assert stored_erc20_eor_data is not None

    # convert realtime retrieved abi and stored data to str, hash and compare the value
    # confirmations changes for every call, so we can't perform hash compare
    # assert hash(str(rt_erc20_eoa)) == hash(str(stored_erc20_eor_data))


def test_get_erc721_token_transfer_events_by_address(eth_ext):
    rt_erc721_eoa = eth_ext.get_erc721_token_transfer_events_by_address(
        "0x28729369d337861D6470db92a752b4835626DF99", force_get=True)

    # get data from the json file
    f = open(f"{TEST_DATA_DIR}/erc721_eoa.json")
    stored_erc721_eor_data = json.load(f)

    assert rt_erc721_eoa is not None
    assert stored_erc721_eor_data is not None

    # convert realtime retrieved abi and stored data to str, hash and compare the value
    # confirmations changes for every call, so we can't perform hash compare
    assert hash(str(rt_erc721_eoa)) == hash(str(stored_erc721_eor_data))


def test_get_eth_balance_eoa_addresses(eth_ext):
    rt_eoa_balance = eth_ext.get_eth_balance_eoa_addresses(["0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a",
                                                           "0x63a9975ba31b0b9626b34300f7f627147df1f526",
                                                            "0x198ef1ec325a96cc354c7266a038be8b5c558f67"],
                                                           force_get=True)
    # get data from the json file
    f = open(f"{TEST_DATA_DIR}/eoa_balance.json")
    stored_eoa_balance_data = json.load(f)

    assert rt_eoa_balance is not None
    assert stored_eoa_balance_data is not None

    # convert realtime retrieved abi and stored data to str, hash and compare the value
    assert hash(str(rt_eoa_balance)) == hash(str(stored_eoa_balance_data))


def test_get_txns_by_address(eth_ext):
    txns = eth_ext.get_txns_by_address("0x3a3e47a28e53978bea59830fad6a0eb2fc371091",
                                       force_get=True)
    print("txns")


def test_get_contract_abi(eth_ext):
    abi = eth_ext.get_contract_abi("0x3a3e47a28e53978bea59830fad6a0eb2fc371091",
                                   force_get=True)
    assert abi is None


def test_all_first_level(eth_ext):
    abi = eth_ext.get_contract_abi(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    assert abi is not None
    first_txn = eth_ext.get_first_txn_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    txn = eth_ext.get_txns_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    int_txn = eth_ext.get_internal_txns_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    log = eth_ext.get_log_by_contract(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)

    # erc20 functions
    erc_20_transfer_events_for_eoa = eth_ext.get_erc20_token_transfer_events_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    erc_20_transfer_events_for_contract = eth_ext.get_erc20_token_transfer_events_by_contract_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)

    # erc721 functions
    erc721_transfer_events_for_eoa = eth_ext.get_erc721_token_transfer_events_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    erc721_transfer_events_for_contract = eth_ext.get_erc721_token_transfer_events_by_contract_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)

    # token functions
    token_supply = eth_ext.get_total_token_supply_by_contract_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    eoa_balance_for_token_contract = eth_ext.get_eoa_acc_balance_by_token_and_contract_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "", force_get=True)
    tok_info = eth_ext.get_token_info_contract(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",force_get=True)


# erc20 contract:0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 contract deployer: 0x95ba4cf87d6723ad9c0db21737d862be80e93911
# erc721 nft contract:0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D contract deployer:0x7bB358144dAF69C9FEF7b72d4bD15f29Ba8e729f
def test_all_erc20_contract_address(eth_ext):
    '''abi = eth_ext.get_contract_abi(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    assert abi is not None
    txn = eth_ext.get_txns_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    int_txn = eth_ext.get_internal_txns_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    log = eth_ext.get_log_by_contract(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)


    erc_20_transfer_events_for_eoa = eth_ext.get_erc20_token_transfer_events_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    erc_20_transfer_events_for_contract = eth_ext.get_erc20_token_transfer_events_by_contract_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)   
    erc20_transfer_events_for_contract_eoa = eth_ext.get_erc20_token_transfer_events_by_contract_eoa_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "0x95ba4cf87d6723ad9c0db21737d862be80e93911", force_get=True)


    erc721_transfer_events_for_eoa = eth_ext.get_erc721_token_transfer_events_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    erc721_transfer_events_for_contract = eth_ext.get_erc721_token_transfer_events_by_contract_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    erc721_transfer_events_for_contract_eoa = eth_ext.get_erc721_token_transfer_events_by_contract_eoa_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "0x95ba4cf87d6723ad9c0db21737d862be80e93911", force_get=True)       

    eoa_balance = eth_ext.get_eth_balance_eoa_addresses(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    token_supply = eth_ext.get_total_token_supply_by_contract_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)
    erc721_transfer_events_for_eoa = eth_ext.get_erc721_token_transfer_events_by_address(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", force_get=True)'''
    eoa_balance_for_token_contract = eth_ext.get_total_token_supply_by_contract_address(
        "0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a", force_get=True)
    print("test")
