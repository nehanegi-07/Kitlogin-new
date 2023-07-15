"""
Created on June 06th 2022
__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""

import logging
import os
from sca.extractor.ethextract import EthExtractor
from sca.transformer.trans import Transformer
from sca.analytic.conanalyze import ContractAnalyzer
from sca.common.storage import LocalStore
from sca.common.config import ConfigHolder


class Pipeline:
    """
    This class creates extractor, transformer, and analyzer packages to extract, transform and
    performs analysis for an Ethereum Contract
    """
    ether_scan = None
    trans = None
    store = None
    config = None

    def __init__(self, customer, file_name, hex_address):
        assert customer is not None
        assert file_name is not None
        assert hex_address is not None
        logger = logging.getLogger(__name__)
        config = ConfigHolder(file_name)
        self.store = LocalStore(config, customer)
        self.ether_scan = EthExtractor(config, self.store)
        self.trans = Transformer(config, self.store)
        # self.ca = ContractAnalyzer(config, self.store, hex_address)
        self.hex_address = hex_address 


    def start(self, force_get):
        self.ether_scan.get_txns_by_address(self.hex_address, force_get=force_get)
        self.ether_scan.get_contract_abi(self.hex_address, force_get=force_get)
        self.ether_scan.get_internal_txns_by_address(self.hex_address, force_get= force_get)
        self.ether_scan.get_erc20_token_transfer_events_by_address(self.hex_address, force_get=force_get)
        self.ether_scan.get_erc721_token_transfer_events_by_address(self.hex_address, force_get=force_get)
        self.ether_scan.get_total_token_supply_by_contract_address(self.hex_address, force_get=force_get)
        self.ether_scan.get_log_by_contract(self.hex_address, force_get=force_get)
        self.ether_scan.get_token_info_contract(self.hex_address, force_get=force_get)
        self.ether_scan.get_erc20_token_transfer_events_by_contract_address(self.hex_address, force_get=force_get)
        self.ether_scan.get_erc721_token_transfer_events_by_contract_address(self.hex_address, force_get=force_get)

        # self.ether_scan.get_erc20_token_transfer_events_by_contract_eoa_address(self.contract_address, self.owner_address, force_get=force_get)
        # self.ether_scan.get_erc721_token_transfer_events_by_contract_eoa_address(self.contract_address, self.owner_address, force_get=force_get)
        # self.ether_scan.get_eth_balance_eoa_addresses
        # self.ether_scan.get_eoa_acc_balance_by_token_and_contract_address




        # get all the JSONs
        print("Creating JSONs=",self.store.get_extract_dir())
        all_json = self.store.create_json_dict(self.store.get_extract_dir())

        return all_json





"""
path = os.getcwd() + "/sca/resource/" + "sca_config.ini"
pl = Pipeline("test", path, "0xd4f11C30078d352354c0B17eAA8076C825416493")
pl.start(force_get=True)
"""
