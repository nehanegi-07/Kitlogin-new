"""
Created on June 10th 2022

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""

import logging
import os
import pandas as pd
from sca.common.storage import BLOCKCHAIN_FILE
from sca.common.storage import Storage
from sca.common.config import ConfigHolder
from sca.common.util import ScaUtil


class ContractAnalyzer:
    customer = None
    contract = None
    txn_df = None
    GWEI_TO_ETH = 1 / (10 ** 9)
    WEI_TO_ETH = 1 / (10 ** 18)

    def __init__(self, config: ConfigHolder, storage: Storage, owner_address: str, contract_address: str):
        """
        Create ContractAnalyzer with ConfigHolder and Storage
        Parameters
        ----------
        config ConfigHolder
        storage Storage
        """
        logger = logging.getLogger(__name__)
        assert config is not None
        assert Storage is not None
        ContractAnalyzer.config = config
        ContractAnalyzer.storage = storage
        ContractAnalyzer.util = ScaUtil(config, storage, owner_address, contract_address)

    def analyze(self, address: str):
        """
        For the passed address performs following analytic.
        - It converts gas_x (transaction gas) from GWEI to ETH
        - Converts transaction gasPrice to ETH
        - From address (from_x) from transaction s identified either EOA or Contract address
        - Identifies transaction to address (to_x) txn_type
        - Identifies from_x and to_x from transaction acc_type

        Stores the data in the file specified BLOCKCHAIN_FILE.ANT.name

        Parameters
        ----------
        address - Used to get the file BLOCKCHAIN_FILE.FULL_TXN.name for the address
        """
        txn_df = ContractAnalyzer.storage.retrieve_trans_data(BLOCKCHAIN_FILE.FULL_TXN.name, address)
        txn_df['gas_x'] = txn_df['gas_x'] * ContractAnalyzer.GWEI_TO_ETH
        txn_df['gasPrice'] = txn_df['gasPrice'] * ContractAnalyzer.GWEI_TO_ETH
        txn_df['value_y'] = txn_df['value_y'] * ContractAnalyzer.WEI_TO_ETH
        txn_df['from_type'] = txn_df['from_x'].apply(ContractAnalyzer.util.is_contract)
        txn_df['txn_type'] = txn_df.apply(lambda x: ContractAnalyzer.util.find_txn_type(x.from_type, x.to_x), axis=1)
        txn_df['acc_type'] = txn_df.apply(lambda x: ContractAnalyzer.util.find_acc_type(x.from_type, x.from_x, x.to_x),
                                          axis=1)

        ContractAnalyzer.storage.store_analytic_data(BLOCKCHAIN_FILE.ANT.name, address, txn_df)

