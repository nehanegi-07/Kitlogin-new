"""
Created on June 15th 2022
__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""


from abc import abstractmethod
from sca.common.config import ConfigHolder
import logging
import os.path
import json
import pathlib
from enum import Enum
import pandas as pd

BLOCKCHAIN_FILE = Enum(
    'BLOCKCHAIN_FILE', 'TXN INT_TXN ABI  LOG  ERC20_ADD ERC721_ADD \
        EOA_BALANCE EOA_TOK_BALANCE ERC20_CONTRACT ERC20_CONTRACT_EOA \
        ERC721_CONTRACT_EOA ERC721_CONTRACT CONTRACT_TOK_BALANCE FST_TXN TOKEN')


class Storage:
    '''
    Abstract class that handles file storing to local drive and S3. It creates following directory
    structure under/data
    <customer_name>/extract - stores all the extract files in the format *_address_*.json
    <customer_name>/trans - stores all the transformed files in the format *_address_*.csv
    <customer_name>/analytic - stores all the analytical files in the format *_address_*.csv

    '''
    config = None

    def __init__(self, con, customer):
        assert con is not None
        assert customer is not None

        Storage.config = con
        self.customer = customer

        self.logger = logging.getLogger(__name__)
        self.log_level = Storage.config.get_value("log_level")
        if self.log_level == "info":
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.DEBUG)

        # if the location is local then create dir locally
        # if not create dir in S3
        if Storage.config.get_value("location") == "local":
            # create dir structure in local computer
            self.create_dir()
        else:
            # create dir structure in S3
            print("yet to code")

    @abstractmethod
    def store_extract_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str, data):
        pass

    @abstractmethod
    def retrieve_extract_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str):
        pass

    @abstractmethod
    def store_trans_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str, df: pd.DataFrame):
        pass

    @abstractmethod
    def retrieve_trans_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str):
        pass

    @abstractmethod
    def store_analytic_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str, df: pd.DataFrame):
        pass

    
    def scan_dir_for_extract_files(self):
        # Create an empty list to store the file names
        file_names = []

        # Scan the directory for all files
        dir_path = self.get_extract_dir()

        for file in os.listdir(dir_path):
            # Check if the file is a regular file (not a directory or a special file)
            if os.path.isfile(os.path.join(dir_path, file)):
                # Append the file name to the list
                file_names.append(file)

        # Return the list of file names
        return file_names
    
    def get_extract_dir(self):
        return (
            f"{os.getcwd()}/sca/data/"
            + self.customer
            + "/extract/"
        )
    
    def read_json_file(self, file_path):
        assert file_path is not None
        # Open the file for reading
        with open(file_path, 'r') as file:
            # Read the contents of the file as a string
            file_contents = file.read()
            return json.loads(file_contents)
        
    def create_json_dict(self, dir_path):
        assert dir_path is not None
        # Get the list of file names in the directory
        file_names = self.scan_dir_for_extract_files()
        # Create an empty dictionary to store the JSON contents
        json_dict = {}

        # Iterate through the file names
        for file_name in file_names:
            # Get the full path to the file
            file_path = os.path.join(dir_path, file_name)
            # Read the JSON contents of the file
            json_contents = self.read_json_file(file_path)
            # Add the JSON contents to the dictionary with the file name as the key
            json_dict[file_name] = json_contents

        # Return the dictionary
        return json_dict


    def get_extract_file_name(self, blockchain_file: BLOCKCHAIN_FILE, address: str) -> str:
        file_name = None
        if Storage.config.get_value("location") == "local":
            file_name = self.blockchain_file_finder(blockchain_file)
        else:
            print("yet to code S3")
        return (
            f"{os.getcwd()}/sca/data/"
            + self.customer
            + "/extract/"
            + address
            + file_name
        )

    def get_trans_file_name(self, blockchain_file: BLOCKCHAIN_FILE, address: str) -> str:
        file_name = None
        if Storage.config.get_value("location") == "local":
            file_name = self.blockchain_file_finder(blockchain_file)
        else:
            print("yet to code S3")
        return (
            f"{os.getcwd()}/sca/data/"
            + self.customer
            + "/trans/"
            + address
            + file_name
        )

    def blockchain_file_finder(self, blockchain_file: BLOCKCHAIN_FILE) -> str:
        """
        Converts enum to file name text
        """
        file_name = None
        if blockchain_file == BLOCKCHAIN_FILE.TXN.name:
            file_name = Storage.config.get_value("txn_file")
        elif blockchain_file == BLOCKCHAIN_FILE.INT_TXN.name:
            file_name = Storage.config.get_value("internal_txn_file")
        elif blockchain_file == BLOCKCHAIN_FILE.ABI.name:
            file_name = Storage.config.get_value("abi_file")
        elif blockchain_file == BLOCKCHAIN_FILE.LOG.name:
            file_name = Storage.config.get_value("log_file")
        elif blockchain_file == BLOCKCHAIN_FILE.ERC20_ADD.name:
            file_name = Storage.config.get_value("erc20_add_file")
        elif blockchain_file == BLOCKCHAIN_FILE.ERC721_ADD.name:
            file_name = Storage.config.get_value("erc721_add_file")
        elif blockchain_file == BLOCKCHAIN_FILE.EOA_BALANCE.name:
            file_name = Storage.config.get_value("eoa_balance_file")
        elif blockchain_file == BLOCKCHAIN_FILE.EOA_TOK_BALANCE.name:
            file_name = Storage.config.get_value("eoa_tok_balance_file")
        elif blockchain_file == BLOCKCHAIN_FILE.CONTRACT_TOK_BALANCE.name:
            file_name = Storage.config.get_value("contract_tok_bal_file")            
        elif blockchain_file == BLOCKCHAIN_FILE.ERC20_CONTRACT.name:
            file_name = Storage.config.get_value("erc20_contract_file")        
        elif blockchain_file == BLOCKCHAIN_FILE.ERC20_CONTRACT_EOA.name:
            file_name = Storage.config.get_value("erc20_contract_eoa_file")         
        elif blockchain_file == BLOCKCHAIN_FILE.ERC721_CONTRACT_EOA.name:
            file_name = Storage.config.get_value("erc721_contract_eoa_file")       
        elif blockchain_file == BLOCKCHAIN_FILE.ERC721_CONTRACT.name:
            file_name = Storage.config.get_value("erc721_contract_file")  
        elif blockchain_file == BLOCKCHAIN_FILE.FST_TXN.name:
            file_name = Storage.config.get_value("first_txn_file")   
        elif blockchain_file == BLOCKCHAIN_FILE.TOKEN.name:
            file_name = Storage.config.get_value("token_info_file")                                        
        return file_name

    def create_dir(self):
        """
        Create dir structure for extract, trans, and analytic for the given customer
        """
        # check if the dir with customer exist, if not create new
        if not os.path.exists(f"{os.getcwd()}/sca/data/" + self.customer):
            os.makedirs(f"{os.getcwd()}/sca/data/" + self.customer)
        if not os.path.exists(
            f"{os.getcwd()}/sca/data/" + self.customer + "/extract/"
        ):
            os.makedirs(((f"{os.getcwd()}/sca/data/" + self.customer) + "/extract/"))
        if not os.path.exists(
            f"{os.getcwd()}/sca/data/" + self.customer + "/analytic/"
        ):
            os.makedirs(((f"{os.getcwd()}/sca/data/" + self.customer) + "/analytic/"))
        if not os.path.exists(
            f"{os.getcwd()}/sca/data/" + self.customer + "/trans/"
        ):
            os.makedirs(((f"{os.getcwd()}/sca/data/" + self.customer) + "/trans/"))


class LocalStore(Storage):
    '''
    LocalStore class to store files in local drive
    '''

    def __init__(self, config, customer):
        super().__init__(config, customer)

    # overriding abstract method
    def store_extract_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str, data):
        """
        Store data extracted from Blockchain through package extractor. It creates the file
        in /extract dir
        Parameters
        ----------
        blockchain_file
        address
        data
        """
        assert blockchain_file is not None
        assert address is not None
        assert data is not None
        path = (
            f"{os.getcwd()}/sca/data/"
            + self.customer
            + "/extract/"
            + address
            + self.blockchain_file_finder(blockchain_file)
        )
        with open(path, 'w') as fout:
            json.dump(data, fout)

    # overriding abstract method
    def store_trans_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str, df: pd.DataFrame):
        """
        Stores data extracted from extractor package and transformed for analyic work. It creates the file
        in /trans dir
        Parameters
        ----------
        blockchain_file
        address
        df
        """
        assert blockchain_file is not None
        assert df is not None
        # store csv files
        file_name = self.blockchain_file_finder(
            blockchain_file).replace(".json", ".csv")
        path = f"{os.getcwd()}/sca/data/" + self.customer + "/trans/" + address
        df.to_csv(path + file_name, index=False)

    # overriding abstract method
    def store_analytic_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str, df: pd.DataFrame):
        """
        Stores the analytic data. It creates the file in /analytic dir
        Parameters
        ----------
        blockchain_file
        address
        df
        """
        assert blockchain_file is not None
        assert df is not None
        file_name = self.blockchain_file_finder(blockchain_file)
        path = (
            (f"{os.getcwd()}/sca/data/" + self.customer + "/analytic/") + address
        ) + file_name
        df.to_csv(path + file_name, index=False)

    # overriding abstract method
    def retrieve_extract_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str):
        """
        Retrieves data from the specified file in /extract folder
        Parameters
        ----------
        blockchain_file
        address

        Returns
        -------

        """
        assert blockchain_file is not None
        assert address is not None
        file_name = self.get_extract_file_name(blockchain_file, address)
        return pathlib.Path(file_name).read_text()

    # overriding abstract method
    def retrieve_trans_data(self, blockchain_file: BLOCKCHAIN_FILE, address: str) -> pd.DataFrame:
        """
        Retrieves data from the specified file in /trans folder
        Parameters
        ----------
        blockchain_file
        address

        Returns
        -------

        """
        assert blockchain_file is not None
        assert address is not None
        file_name = self.get_trans_file_name(
            blockchain_file, address).replace(".json", ".csv")
        # Read in the file contents as DataFrame
        return pd.read_csv(file_name)


class S3Store(Storage):
    def __init__(self, config, customer):
        super().__init__(config, customer)
