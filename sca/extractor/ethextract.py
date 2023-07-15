"""
https://github.com/pcko1/etherscan-python
A minimal, yet complete, Python API for Etherscan.io

Created on June 6th 2022

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""


import logging
import sys
import json
from etherscan.etherscan import Etherscan
import traceback
import requests
from sca.common.storage import BLOCKCHAIN_FILE

import pandas as pd



class EthExtractor:
    '''
    This class uses Etherscan from etherscan.etherscan to retrieve data from
    Ethereum blokchain.

    '''
    config = None
    storage = None

    def __init__(self, config, storage):
        '''
        Create BlackChainExtractor with file_names

        Parameters
        ----------
        customer : TYPE str
        Name of the customer that needs contract analytic. If
        directory doesn't exist, new directory with passed-in customer will be
        created
        file_name : TYPE
            Configuration file names

        Returns
        -------
        None.

        '''
        assert config is not None
        assert storage is not None

        EthExtractor.config = config
        EthExtractor.storage = storage

        self.logger = logging.getLogger(__name__)
        self.log_level = EthExtractor.config.get_value("log_level")

        if self.log_level == "info":
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.DEBUG)

        api_url = EthExtractor.config.get_value("ether_scan_api_url")
        self.eth_scan = Etherscan(api_url)

    def get_config_value(self, key):
        '''
        Get the value associated with the parameter "key" from the ConfigHolder
        associated with the BlackChainExtractor

        Parameters
        ----------
        key : str
            Name of the config parameter defined in the config file

        Returns
        -------
        str
            Value of the parameter associated with the key,
            defined in the config file


        '''
        assert key is not None
        return EthExtractor.ch.get_value(key)

    def get_first_txn_by_address(self, contract_address_hex: str, force_get=False):
        """
        For the given address_hex get very first txn to find the contract deployer

        Parameters
        ----------
        address_hex - smart contract address or EOA address
        force_get - True or False

        Returns list of  JSON
    def get_normal_txs_by_address_paginated(
        address: str, page: int, offset: int, startblock: int, endblock: int, sort: str,

        """

        assert contract_address_hex is not None
        txn_result = []
        if force_get is True:
            txn_result = self.eth_scan.get_normal_txs_by_address_paginated(
                contract_address_hex, 1,1,0, 99999999, "asc")
            EthExtractor.storage.store_extract_data(
                BLOCKCHAIN_FILE.FST_TXN.name, contract_address_hex, txn_result)

        return txn_result        

    def get_txns_by_address(self, contract_address_hex: str, start_block: int = 0, end_block: int = 99999999, force_get=False):
        """
        For the given contract_address_hex address get all the normal transactions. Normal
        txns are transactions crated either by EOA address or contract address to
        other contract address. For contract address retrieves txns for that contract.
        For EOA address, returns all txns for that EOA address

        In a single call Etherscan returns max of 10k txns. To get all the txns, use sort=desc, 
        start_block:int=0, end_block:int=99999999, get first batch of txns, go the <last bllcokNumber> from the batch 
        send second call to Etherscan API with start_block=<last bllcokNumber>, end_block:int=99999999 get the result.
        Continue the above step until you get less than 10K records for the API call. Combine all of them that will give
        you all the txns for the contract_address_hex



        Parameters
        ----------
        address_hex - smart contract address or EOA address
        force_get - True or False

        Returns list of following JSON
        {
            "blockNumber":"14879194",
            "timeStamp":"1654007319",
            "hash":"0x0fd00891d469ef1cddcf3635d0d4e5fa632064e93f1cce63c5fe3b220c9a5fc7",
            "nonce":"3",
            "blockHash":"0x2ef3fa5224c09ecf56f4f71b1e17ce2a296866bfcafee64011f51543a30223af",
            "transactionIndex":"243",
            "from":"0x1a20a03f0b324388072993fa604c06b68196020f",
            "to":"0xd4f11c30078d352354c0b17eaa8076c825416493",
            "value":"0",
            "gas":"68850",
            "gasPrice":"40236381812",
            "isError":"0",
            "txreceipt_status":"1",
            "input":"0x7b9e7433",
            "contractAddress":"",
            "cumulativeGasUsed":"18565105",
            "gasUsed":"45900",
            "confirmations":"1609062",
            "methodId":"0x7b9e7433",
            "functionName":"togglehitlistSale()"
        },

        """

        assert contract_address_hex is not None
        assert start_block is not None
        assert end_block is not None
        txn_result = []
        if force_get is True:
            txn_result = self.eth_scan.get_normal_txs_by_address(
                contract_address_hex, 0, 99999999, "desc")
            EthExtractor.storage.store_extract_data(
                BLOCKCHAIN_FILE.TXN.name, contract_address_hex, txn_result)

        return txn_result

    def get_internal_txns_by_address(self, contract_address_hex: str, start_block: int = 0, end_block: int = 99999999, force_get=False):
        """
        For the given contract_hex address get all the internal transactions. Internal txns
        are started by the normal txns

        Parameters
        ----------
        contract_hex - smart contract address
        force_get - True or False

        Returns following JSON list
        {
            "blockNumber":"14879665",
            "timeStamp":"1654013473",
            "hash":"0xc15dad995ca955bb319b3a3dd9d8017f17968985a6a43623df20f41b726f5462",
            "from":"0xd4f11c30078d352354c0b17eaa8076c825416493",(parent_txn)
            "to":"0x1333e81c131e1d1d0e8bd42eca5e45acd0ce1de3", (contractor_creator)
            "value":"5960000000000000742",
            "contractAddress":"",
            "input":"",
            "type":"call",
            "gas":"2300",
            "gasUsed":"0",
            "traceId":"0",
            "isError":"0",
            "errCode":""
        }
        """
        assert contract_address_hex is not None
        if force_get is True:
            txn_result = self.eth_scan.get_internal_txs_by_address(
                contract_address_hex, 0, 99999999, "desc")
            EthExtractor.storage.store_extract_data(
                BLOCKCHAIN_FILE.INT_TXN.name, contract_address_hex, txn_result)

    def is_contract_adress(self, contract_address_hex) -> bool:
        """
        Return True if the passed in contract_address_hex is a contract. If it is EOA then 
        returns False
        """
        assert contract_address_hex is not None
        abi = self.get_contract_abi(contract_address_hex, True)
        return abi is not None

    def get_contract_abi(self, contract_address_hex, force_get=False):
        """
        For the given contract, get contract ABI. If force_get is true it gets the ABI, if it is False
        and the file not exist it gets the ABI. If it is false and the file exist doesn't get the ABI.
        If the passed contract_address_hex is EOA or contract couldn't find it then it returns None
        Parameters
        ----------
        contract_hex: address of the contract in hex
        force_get: True or False
        """

        assert contract_address_hex is not None
        contract_abi = None
        if force_get is True:
            try:
                contract_abi = self.eth_scan.get_contract_abi(contract_address_hex)
                contract_abi = json.loads(contract_abi)
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.ABI.name, contract_address_hex, contract_abi)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return contract_abi

    def get_log_by_contract(self, contract_address_hex, force_get=False):
        assert contract_address_hex is not None
        log_data = None

        if force_get is True:
            file_name = EthExtractor.storage.get_extract_file_name(
                BLOCKCHAIN_FILE.LOG.name, contract_address_hex)
            log_url = EthExtractor.config.get_value("ethplorer_url_log")
            log_url = log_url.replace("ADRS", contract_address_hex)
            log_data = requests.get(log_url)
            log_data = json.loads(log_data.text)
            EthExtractor.storage.store_extract_data(
                BLOCKCHAIN_FILE.LOG.name, contract_address_hex, log_data.get("result"))

        return log_data.get("result")

    def get_token_info_contract(self, contract_address_hex, force_get=False):
        """
        For the given contract, get the token info. If force_get is true it gets the erc20,
        if it is False and the file not exist it gets the erc721. If it is false and the file
        exist doesn't get the erc721. Uses ethplorer API
        Parameters
        ----------
        contract_address_hex: address of the contract in hex
        force_get: True or False
        """
        assert contract_address_hex is not None
        data = None

        if force_get is True:
            file_name = EthExtractor.storage.get_extract_file_name(
                BLOCKCHAIN_FILE.TOKEN.name, contract_address_hex)
            ethplorer_url = EthExtractor.config.get_value("ethplorer_url")
            ethplorer_api = EthExtractor.config.get_value("ethplorer_api")
            data = requests.get(
                f'{ethplorer_url}/getTokenInfo/{contract_address_hex}?apiKey={ethplorer_api}'
            )

            data = json.loads(data.text)
            EthExtractor.storage.store_extract_data(
                BLOCKCHAIN_FILE.TOKEN.name, contract_address_hex, data)

        return data        

    def get_erc20_token_transfer_events_by_address(self, contract_address_hex: str, start_block: int = 0, end_block: int = 99999999, force_get=False):
        """
        For the given address return erc20 token transfers max of 10K. This method returns erc20 token transfers that originates from the
        passed-in address_hex. See "from" in the example below:
        Parameters
        ----------
        eoa_address_hex:  contract address OR EOA address
        force_get: True or False
        All the returned JSON will have same "from" address
        

        Eg
            {
                "blockNumber": "16626265",
                "timeStamp": "1676368979",
                "hash": "0xa9e3ad9492344f619c246a44c64140218be4c0ea1dd847d08d883cc5bda3b856",
                "nonce": "44",
                "blockHash": "0xabcaddf781fb95ae9b74510e9ba53a48292fb24a0e985cce05cce737a13442f5",
                "from": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                "contractAddress": "0xd8daa146dc3d7f2e5a7df7074164b6ad99bed260",
                "to": "0xeb78ae2696c5a4ca99521ed9e134dc01e4d543e1",
                "value": "49990000000",
                "tokenName": "",
                "tokenSymbol": "",
                "tokenDecimal": "0",
                "transactionIndex": "7",
                "gas": "171112",
                "gasPrice": "22000000000",
                "gasUsed": "140937",
                "cumulativeGasUsed": "1439389",
                "input": "deprecated",
                "confirmations": "18275"
            },
            {
                "blockNumber": "16625926",
                "timeStamp": "1676364875",
                "hash": "0x94c2aa11c31a89cacf0ed72237019b03485b42b63c5c63610ea85a8ee3ef1fd0",
                "nonce": "43",
                "blockHash": "0x18ecedfe70102bc12dfc76fd14566208c313914c05f9316599cfdd00faf48ed4",
                "from": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                "contractAddress": "0xd8daa146dc3d7f2e5a7df7074164b6ad99bed260",
                "to": "0xeb78ae2696c5a4ca99521ed9e134dc01e4d543e1",
                "value": "10000000",
                "tokenName": "",
                "tokenSymbol": "",
                "tokenDecimal": "0",
                "transactionIndex": "19",
                "gas": "191943",
                "gasPrice": "22000000000",
                "gasUsed": "158025",
                "cumulativeGasUsed": "1086577",
                "input": "deprecated",
                "confirmations": "18614"
            }
        """

        assert contract_address_hex is not None
        erc20 = None
        if force_get is True:
            try:
                erc20 = self.eth_scan.get_erc20_token_transfer_events_by_address(contract_address_hex,
                                                                                 start_block, end_block, "desc")
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.ERC20_ADD.name, contract_address_hex, erc20)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return erc20

    def get_erc20_token_transfer_events_by_contract_address(self, contract_address_hex: str, force_get=False):
        """
        For the given address return erc20 token transfers max of 10K. This method returns erc20 token transfers that passes through the
        passed-in address_hex. See "contractAddress" in the example below, which is passed-in address_hex. Both JSONs have different "from"
        address.
        Parameters
        ----------
        eoa_address_hex:  address
        force_get: True or False
        Return 10K limit

        E.g.
            {
                "blockNumber": "16644539",
                "timeStamp": "1676589671",
                "hash": "0x4d6d0e71ac6b9aadd0f999222c2ef6568623cf2b7512d4e718b307dab34fed85",
                "nonce": "73060",
                "blockHash": "0x08c4fa10272a6ae32317a4d6400257d435e6ba02e682ba36a90996df3167916d",
                "from": "0x0000000000000000000000000000000000000000",
                "contractAddress": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                "to": "0x55fe002aeff02f77364de339a1292923a15844b8",
                "value": "3472080000",
                "tokenName": "USD Coin",
                "tokenSymbol": "USDC",
                "tokenDecimal": "6",
                "transactionIndex": "151",
                "gas": "200000",
                "gasPrice": "35215492076",
                "gasUsed": "57359",
                "cumulativeGasUsed": "10601728",
                "input": "deprecated",
                "confirmations": "1"
            },
            {
                "blockNumber": "16644539",
                "timeStamp": "1676589671",
                "hash": "0x0221f2f9359170d6bf71b5c3ec405af30a2ae49aab189ff104499e7828a84e0f",
                "nonce": "54429",
                "blockHash": "0x08c4fa10272a6ae32317a4d6400257d435e6ba02e682ba36a90996df3167916d",
                "from": "0x3666f603cc164936c1b87e207f36beba4ac5f18a",
                "contractAddress": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                "to": "0xa6a688f107851131f0e1dce493ebbebfaf99203e",
                "value": "10579123",
                "tokenName": "USD Coin",
                "tokenSymbol": "USDC",
                "tokenDecimal": "6",
                "transactionIndex": "149",
                "gas": "500000",
                "gasPrice": "35267492076",
                "gasUsed": "142896",
                "cumulativeGasUsed": "10523369",
                "input": "deprecated",
                "confirmations": "1"
            },
        """

        assert contract_address_hex is not None
        erc20 = None
        if force_get is True:
            try:
                erc20 = self.eth_scan.get_erc20_token_transfer_events_by_contract_address_paginated(
                    contract_address_hex, 1, 10000, "desc")
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.ERC20_CONTRACT.name, contract_address_hex, erc20)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return erc20

    def get_erc20_token_transfer_events_by_contract_eoa_address(self, eoa_address_hex: str, address_hex: str, force_get=False):
        """
        Parameters
        ----------
        eoa_address_hex:  address
        force_get: True or False
        """

        assert eoa_address_hex is not None
        erc20 = None
        if force_get is True:
            try:
                erc20 = self.eth_scan.get_erc20_token_transfer_events_by_address_and_contract_paginated(
                    eoa_address_hex, address_hex, 1, 10000, "desc")
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.ERC20_CONTRACT_EOA.name, eoa_address_hex, erc20)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return erc20

    def get_erc721_token_transfer_events_by_address(self, address_hex: str, start_block: int = 0, end_block: int = 99999999, force_get=False):
        """
        For the given EOA address return erc721 token transfers
        Parameters
        ----------
        address_hex: contract address OR EOA address
        force_get: True or False
        """

        assert address_hex is not None
        erc721 = None
        if force_get is True:
            try:
                erc721 = self.eth_scan.get_erc721_token_transfer_events_by_address(address_hex,
                                                                                   start_block, end_block, "desc")
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.ERC721_ADD.name, address_hex, erc721)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return erc721

    def get_erc721_token_transfer_events_by_contract_address(self, contract_address:str, force_get=False):
        """
        For the given EOA address return erc721 token transfers
        Parameters
        10k limit
        ----------
        eoa_address_hex: EOA address
        force_get: True or False
        """

        assert contract_address is not None
        erc721 = None
        if force_get is True:
            try:
                erc721 = self.eth_scan.get_erc721_token_transfer_events_by_contract_address_paginated(contract_address,
                                                                                   1, 10000, "desc")
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.ERC721_CONTRACT.name, contract_address, erc721)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return erc721


    def get_erc721_token_transfer_events_by_contract_eoa_address(self, contract_address:str, eoa_address:str, force_get=False):
        """
        For the given EOA address return erc721 token transfers
        Parameters
        ----------
        eoa_address_hex: EOA address
        force_get: True or False
        """

        assert contract_address is not None
        assert eoa_address is not None
        erc721 = None
        if force_get is True:
            try:
                erc721 = self.eth_scan.get_erc721_token_transfer_events_by_address_and_contract_paginated(contract_address,eoa_address,
                                                                                   1, 10000, "desc")
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.ERC721_CONTRACT_EOA.name, contract_address, erc721)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return erc721        



    def get_eth_balance_eoa_addresses(self, eoa_address_hexs, force_get=False):
        """
        For the given EOA address return erc721 token transfers
        Parameters
        ----------
        eoa_address_hex: EOA address
        force_get: True or False
        Returns following JSON for each of the passed EOA address
          {
            "account":"0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a",
            "balance":"40891626854930000000999" is in wei. Convert to ETH=balance/10^5
        }
        """

        assert eoa_address_hexs is not None
        eoa_balances = None
        if force_get is True:
            try:
                eoa_balances = self.eth_scan.get_eth_balance_multiple(
                    eoa_address_hexs)
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.EOA_BALANCE.name, eoa_address_hexs[0], eoa_balances)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return eoa_balances

    def get_total_token_supply_by_contract_address(self, address_hex: str, force_get=False):
        """
        For the given address_hex return total token supply
        Parameters
        ----------
        eoa_address_hex: EOA address
        force_get: True or False

        Result
        {
        "address":"0x57d90b64a1a57749b0f932f1a3395792e12e7055",
        "name":"Elcoin",
        "decimals":"6",
        "symbol":"",
        "totalSupply":"21265524714464",
        "owner":"",
        "lastUpdated":1619183656,
        "transfersCount":23540,
        "txsCount":5564,
        "issuancesCount":0,
        "holdersCount":4368,
        "ethTransfersCount":1635,
        "price":false,
        "countOps":23540
        }
        """

        assert address_hex is not None
        total_token_supply = None
        if force_get is True:
            try:
                total_token_supply = self.eth_scan.get_total_supply_by_contract_address(
                    address_hex)
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.CONTRACT_TOK_BALANCE.name, address_hex, total_token_supply)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return total_token_supply

    def get_eoa_acc_balance_by_token_and_contract_address(self, contract_address_hex: str, eoa_address_hex: str, force_get=False):
        """
        Etherscan method Get ERC20-Token Account Balance for TokenContractAddress from
        https://docs.etherscan.io/api-endpoints/tokens

        Returns the current EOA balance for the passed-in contract and eoa address. Each contract (token contract) can 
        have multiple eoa accounts and each account will have a balance associated with it.
        Parameters
        ----------
        contract_address_hex: token contract address
        eoa_address_hex: EOA address
        force_get: True or False
        balance=value returned by this method/10^(decimals from get_total_token_supply_by_contract_address function)
        """

        assert contract_address_hex is not None
        assert eoa_address_hex is not None
        total_token_supply = None
        if force_get is True:
            try:
                total_token_supply = self.eth_scan.get_acc_balance_by_token_and_contract_address(
                    contract_address_hex, eoa_address_hex)
                EthExtractor.storage.store_extract_data(
                    BLOCKCHAIN_FILE.EOA_TOK_BALANCE.name, contract_address_hex, total_token_supply)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]
                self.logger.error(
                    f'An error occurred on line {line} in statement {text}',
                    exc_info=True,
                )
        return total_token_supply






