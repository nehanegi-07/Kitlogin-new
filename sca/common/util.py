"""
Created on June 20th 2022

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""
from sca.common.storage import Storage
from sca.common.config import ConfigHolder
from web3 import Web3
from enum import Enum
import numpy as np
import pandas as pd

"""
transaction type tells different from_address and to_address in a transaction
EOA_2_EOA - EOA  send message to other EOA
EOA_2_C - EOA send message to Contract address to execute a instruction
C_2_C - Contract address send message to another Contract address
EOA_2_ - EOA send message to create a new contract. In this case to_address will be null
"""
TXN_TYPE = Enum('TXN_TYPE', 'EOA_2_EOA EOA_2_C EOA_2_ C_2_C')

"""
ADDRESS_TYPE for either from_address OR for to_address
OWNER - Contract Owner which EOA address
CUSTOMER - EOA address who is the owner of the Contract
CONTRACT - Represents Contract address in Blockchain
"""
ADDRESS_TYPE = Enum('ADDRESS_TYPE', 'OWNER CUSTOMER CONTRACT')

"""
TXN_DATA_TYPE is Data sent in transaction can be either contract data or ETH
ETH - sent in message 
CONTRACT - Contract data sent for contract creation
TOKEN - token sent for transfer from one address to other
"""
TXN_DATA_TYPE = Enum('TXN_DATA_TYPE', 'ETH  CONTRACT TOKEN')


class ScaUtil:
    """
    This class identifies TXN_TYPE, ADDRESS_TYPE, and TXN_DATA_TYPE. It takes owner_address (EOA) of 
    a contract and the address of contract stored in Ethereum. This utility helps for a set of transactions
    retrieved for a given contract address.
    """
    def __init__(self, config: ConfigHolder, storage: Storage, owner_address: str, contract_address: str):
        """
        Create ScaUtil object

        Parameters
        ----------
        config
        storage
        """
        assert config is not None
        assert Storage is not None
        ScaUtil.config = config
        ScaUtil.storage = storage
        archivenode_url = config.get_value("archivenode_url")
        self.web3 = Web3(Web3.HTTPProvider(archivenode_url))
        self.owner_address = owner_address
        self.contract_address = contract_address



    def is_contract(self, address: str) -> bool:
        """
        Identifies the passed in address is either EOA or Contract address
        Parameters
        ----------
        address

        Returns
        -------

        """
        if pd.isnull(address):
            return np.nan

        # checlsum cryptographic function that allows users to verify their blockchain addresses to 
        # ensure they are valid and don't contain any typos    
        checksum_address = Web3.toChecksumAddress(address)
        result = self.web3.eth.get_code(checksum_address)
        # if the passed-in address in contract address, it will have code deployed on the contract
        return result != b''


    def find_txn_type(self, from_address: str, to_address: str) -> TXN_TYPE:
        """
        transaction type tells different from_address and to_address in a transaction
        EOA_2_EOA, EOA_2_C, EOA_2_, C_2_C
        """
        assert from_address is not None
        if self.from_address == self.owner_address:
            return TXN_TYPE.EOA_2_
        if self.is_contract(from_address) and self.is_contract(to_address):
            return TXN_TYPE.C_2_C
        if not self.is_contract(from_address) and self.is_contract(to_address):
            return TXN_TYPE.EOA_2_C           
        if not self.is_contract(from_address) and not self.is_contract(to_address):
            return TXN_TYPE.EOA_2_EOA              

    def find_address_type(self, address: str) -> ADDRESS_TYPE:       
        """
        For the passed-in address returns ADDRESS_TYPE
        """
        
        assert address is not None

        if address == self.self.owner_address:
            return ADDRESS_TYPE.OWNER
        if address == self.contract_address:
            return ADDRESS_TYPE.CUSTOMER
        if self.is_contract(address) == True:
            return ADDRESS_TYPE.CONTRACT
        else:
            return ADDRESS_TYPE.CUSTOMER



