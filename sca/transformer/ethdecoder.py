"""
Created on May 26th 2022
from https://gist.github.com/yifeihuang/311d60e8c08b9147d25fd8652d0f6029

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""

import traceback
import sys
from functools import lru_cache
from web3 import Web3
from web3.auto import w3
from web3._utils.events import get_event_data
from eth_utils import event_abi_to_log_topic, to_hex
from hexbytes import HexBytes

import json
import logging

class EthDecoder:
    """
    This class decodes Ethereum transaction and log
    Code copied and modified from https://towardsdatascience.com/decoding-ethereum-smart-contract-data-eed513a65f76
    
    """


    def __init__(self ):
        logger = logging.getLogger(__name__)

    def decode_tuple(self, t, target_field):
        output = {}
        for i in range(len(t)):
            if isinstance(t[i], (bytes, bytearray)):
                output[target_field[i]['name']] = to_hex(t[i])
            elif isinstance(t[i], (tuple)):
                output[target_field[i]['name']] = self.decode_tuple(t[i], target_field[i]['components'])
            else:
                output[target_field[i]['name']] = t[i]
        return output

    def decode_list_tuple(self, l, target_field):
        output = l
        for i in range(len(l)):
            output[i] = self.decode_tuple(l[i], target_field)
        return output

    def decode_list(self, l):
        output = l
        for i in range(len(l)):
            output[i] = to_hex(l[i]) if isinstance(l[i], (bytes, bytearray)) else l[i]
        return output

    def convert_to_hex(self, arg, target_schema):
        """
        utility function to convert byte codes into human readable and json serializable data structures
        """
        output = {}
        for k in arg:
            if isinstance(arg[k], (bytes, bytearray)):
                output[k] = to_hex(arg[k])
            elif isinstance(arg[k], (list)) and len(arg[k]) > 0:
                target = [a for a in target_schema if 'name' in a and a['name'] == k][0]
                if target['type'] == 'tuple[]':
                    target_field = target['components']
                    output[k] = self.decode_list_tuple(arg[k], target_field)
                else:
                    output[k] = self.decode_list(arg[k])
            elif isinstance(arg[k], (tuple)):
                target_field = [a['components'] for a in target_schema if 'name' in a and a['name'] == k][0]
                output[k] = self.decode_tuple(arg[k], target_field)
            else:
                output[k] = arg[k]
        return output

    @lru_cache(maxsize=None)
    def _get_contract(self, address, abi):
        """
        This helps speed up execution of decoding across a large dataset by caching the contract object
        It assumes that we are decoding a small set, on the order of thousands, of target smart contracts
        """
        if isinstance(abi, (str)):
            abi = json.loads(abi)

        contract = w3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)
        return (contract, abi)

    def decode_tx(self, address, input_data, abi):
        """
        For the given address, input_data (data from normal txn), and abi decodes the
        input_data (data sent in message to contract)
        """
        if abi is not None:
            try:
                (contract, abi) = self._get_contract(address, abi)
                # get function name and function parameters from input_data
                func_obj, func_params = contract.decode_function_input(input_data)
                # target_schema is entire function signature
                target_schema = [a['inputs'] for a in abi if 'name' in a and a['name'] == func_obj.fn_name][0]
                decoded_func_params = self.convert_to_hex(func_params, target_schema)
                return (func_obj.fn_name, json.dumps(decoded_func_params), json.dumps(target_schema))
            except Exception:
                traceback.print_exc()
                e = sys.exc_info()[0]
                return ('decode error', repr(e), None)
        else:
            return ('no matching abi', None, None)

    @lru_cache(maxsize=None)
    def _get_topic2abi(self, abi):
        if isinstance(abi, (str)):
            abi = json.loads(abi)

        event_abi = [a for a in abi if a['type'] == 'event']
        return {event_abi_to_log_topic(_): _ for _ in event_abi}


    @lru_cache(maxsize=None)
    def _get_hex_topic(self, t):
        return HexBytes(t)


    def decode_log(self, data, topics, abi):
        if abi is None:
            return ('no matching abi', None, None)
        try:
            return self._extracted_from_decode_log_4(abi, data, topics)
        except Exception:
            return ('decode error', traceback.format_exc(), None)

    # TODO Rename this here and in `decode_log`
    def _extracted_from_decode_log_4(self, abi, data, topics):
        topic2abi = self._get_topic2abi(abi)

        log = {
            'address': None,  # Web3.toChecksumAddress(address),
            'blockHash': None,  # HexBytes(blockHash),
            'blockNumber': None,
            'data': data,
            'logIndex': None,
            'topics': [self._get_hex_topic(_) for _ in topics],
            'transactionHash': None,  # HexBytes(transactionHash),
            'transactionIndex': None
        }
        event_abi = topic2abi[log['topics'][0]]
        evt_name = event_abi['name']

        data = get_event_data(w3.codec, event_abi, log)['args']
        target_schema = event_abi['inputs']
        decoded_data = self.convert_to_hex(data, target_schema)

        return (evt_name, json.dumps(decoded_data), json.dumps(target_schema))
