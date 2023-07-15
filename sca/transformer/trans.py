"""
Created on June 06th 2022
__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""

import logging

from sca.transformer.ethdecoder import EthDecoder
import pandas as pd

from sca.common.storage import BLOCKCHAIN_FILE
from sca.common.storage import Storage
from sca.common.config import ConfigHolder
import sys
import traceback

class Transformer:
    """
    This class decodes Ethereum transaction and log, combines all the data to create a CSV file
    """
    config = None
    storage = None

    def __init__(self, config: ConfigHolder, storage: Storage):
        assert config is not None
        assert storage is not None

        Transformer.config = config
        Transformer.storage = storage

        self.logger = logging.getLogger(__name__)
        self.log_level = Transformer.config.get_value("log_level")

        if self.log_level == "info":
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.DEBUG)

    def transform_txns(self, address: str):
        """
        normal_txns=full txn
        In the Ethereum protocol there's only transactions and message calls. 
        A transaction is a type of message call coming from outside. This method
        finds all the normal transactions for the given contract address. 
        This method calls decode_tx from EthDecoder to decode the transaction
        retrieved from Ethereum.
        """
        assert address is not None
        txn_data = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.TXN.name, address)
        abi = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.ABI.name, address)

        # Convert JSON string with records orient to a Dataframe
        df = pd.read_json(txn_data, orient='records')
        df = df.add_suffix('_txn')

        '''
        This is commented not to decode the input data sent in message call due to decode error.
        eth_decoder = EthDecoder()
        new_cols = ["func_name", "func_parm", "schema"]
        df[new_cols] = None
        for index, row in df.iterrows():
            # Normal transactions created when EOA/contract send message to a contract. The message
            # contains function name, function parameters, and schema

            decoded_input = eth_decoder.decode_tx(address, row["input"], abi)
            df["func_name"][index] = decoded_input[0]
            df["func_parm"][index] = decoded_input[1]
            df["func_sig"][index] = decoded_input[2]

        del df["input"]
        '''
        Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.TXN.name, address, df)

    def transform_internal_txns(self, address: str):    
        """
        An internal transaction is not a real transaction - it has no signature and is not included in the blockchain. 
        It is the result of a contract initiating a value transfer, or calling another contract, typically using 
        the CREATE, CALL, CALLCODE, DELEGATECALL, SELFDESCTUCT  opcodes.Though the internal transactions are not
        included it can be derived

        This method retrieves all the internal transactions for the given contract address data from Storage to 
        CSV
        """
        assert address is not None        
        int_txn_data = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.INT_TXN.name, address)
        # Convert JSON string with records orient to a Dataframe
        df = pd.read_json(int_txn_data, orient='records')
        df = df.add_suffix('_intTxn')

        Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.INT_TXN.name, address, df)

    def transform_logs(self, address: str):
        """
        This method transforms lgos for the given contract address data from Storage to CSV
        """
        assert address is not None   
        int_txn_data = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.LOG.name, address)
        abi = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.ABI.name, address)
        # Convert JSON string with records orient to a Dataframe
        df = pd.read_json(int_txn_data)
        '''
        eth_decoder = EthDecoder()
        new_cols = ["event", "event_parm"]
        df[new_cols] = None
        for index, row in df.iterrows():
            temp = eth_decoder.decode_log(row["data"], row["topics"], abi)
            df["event"][index] = temp[0]
            df["event_parm"][index] = temp[1]

        df = df.rename(columns={'transactionHash': 'hash'})
        '''
        df = df.add_suffix('_logs')

        Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.LOG.name, address, df)

    def transform_contract_tok_info(self, address: str):
        """
        This method transforms contract token balance for the given contract address data from Storage to CSV
        """
        assert address is not None   
        contract_tok_info_data = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.TOKEN.name, address)
        df = pd.read_json(contract_tok_info_data)
        df = df.add_suffix('_tokInfo')

        Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.TOKEN.name, address, df)      


    def transform_first_txn(self, address: str):
        """
        This method transforms first txn data for the given contract address data from Storage to CSV
        """
        assert address is not None       
        first_txn = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.FST_TXN.name, address)
        df = pd.read_json(first_txn)
        df = df.add_suffix('_fstTxn')
        Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.FST_TXN.name, address, df)          


    def transform_erc20_address(self, address: str):
        """
        This method transforms erc20 address data for the given contract address data from Storage to CSV
        """
        assert address is not None           
        erc20_add_data = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.ERC20_ADD.name, address)
        df = pd.read_json(erc20_add_data)
        df = df.add_suffix('_erc20Add')

        Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.ERC20_ADD.name, address, df)             

    def transform_erc721_address(self, address: str):
        """
        This method transforms erc721 address data for the given contract address data from Storage to CSV
        """
        assert address is not None           
        erc721_add_data = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.ERC721_ADD.name, address)
        df = pd.read_json(erc721_add_data)
        df = df.add_suffix('_erc721Add')

        Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.ERC721_ADD.name, address, df)    

    def transform_erc20_contract(self, address: str):
        """
        This method transforms erc20 address data for the given contract address data from Storage to CSV
        """
        assert address is not None           
        try:
            erc20_contract_data = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.ERC20_CONTRACT.name, address)
            df = pd.read_json(erc20_contract_data)
            df = df.add_suffix('_erc20Con')

            Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.ERC20_CONTRACT.name, address, df)          
        except FileNotFoundError:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)  # Fixed format
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]
            self.logger.error(
                f'An error occurred on line {line} in statement {text}',
                exc_info=True,
            )   

    def transform_erc721_contract(self, address: str):
        """
        This method transforms erc721 address data for the given contract address data from Storage to CSV
        """
        assert address is not None           
        try:
            erc721_contract_data = Transformer.storage.retrieve_extract_data(BLOCKCHAIN_FILE.ERC721_CONTRACT.name, address)
            df = pd.read_json(erc721_contract_data)
            df = df.add_suffix('_erc721Con')

            Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.ERC721_CONTRACT.name, address, df)     
        except FileNotFoundError:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)  # Fixed format
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]
            self.logger.error(
                f'An error occurred on line {line} in statement {text}',
                exc_info=True,
            )                         

    def merge_trns_data(self, address: str):
        """
        This function merges txn, internal txn, log data and stores it in Storage
        """
        assert address is not None           
        txn_df = Transformer.storage.retrieve_trans_data(BLOCKCHAIN_FILE.TXN.name, address)
        int_txn_df = Transformer.storage.retrieve_trans_data(BLOCKCHAIN_FILE.INT_TXN.name, address)
        log_df = Transformer.storage.retrieve_trans_data(BLOCKCHAIN_FILE.LOG.name, address)
        # remove same columns from int_txn that already exist in txn
        # int_txn_df.drop(['blockNumber', 'timeStamp'], axis=1, inplace=True)
        full_df = pd.merge(txn_df, int_txn_df, on="hash", how="outer")
        # log_df.drop(['address', 'topics', 'data', 'blockNumber', 'timeStamp', 'gasPrice', 'gasUsed', 'logIndex',
        #             'transactionIndex'], axis=1, inplace=True)
        full_df = pd.merge(full_df, log_df, on="hash", how="outer")
        Transformer.storage.store_trans_data(BLOCKCHAIN_FILE.FULL_TXN.name, address, full_df)

