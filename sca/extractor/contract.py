import json
from web3 import Web3

# Fill in your infura API key here
archivenode_url = 'https://api.archivenode.io/cbeed902-5bf9-44ca-9e31-9e9a58cf0c4e'

web3 = Web3(Web3.HTTPProvider(archivenode_url))
result=web3.eth.get_code('0x6C8f2A135f6ed072DE4503Bd7C4999a1a17F824B')
result_str=result.hex() #0x it is EOA else it is contract
print("result=",result)

# Get it from Etherscan and change true => True and false => False
abi = [{"inputs":[{"internalType":"address[]","name":"addresses","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]

address = '0x990f341946A3fdB507aE7e52d17851B87168017c'

contract = web3.eth.contract(address=address, abi=abi)

# Let's print Name of Token
print("token name=", contract.functions.name().call())
print("token balance=", contract.functions.balanceOf(address).call())

import web3

def get_contract(url, smart_contract_address):
    abi_ = get_abi()
    web3_eth = web3.Web3(web3.Web3.HTTPProvider(url))
    return web3_eth.eth.contract(abi=abi_, address=smart_contract_address)

def get_erc_type(contract):
    is_721 =  contract.functions.supportsInterface(b'\x80\xacX\xcd').call()
    if is_721:
        return "ERC721"
    is_1155 = contract.functions.supportsInterface(b'\xd9\xb6z&').call()
    if is_1155:
        return "ERC1155"
    return None

def get_abi():
    return [{
        "constant": True,
        "inputs": [{
            "internalType": "bytes4",
            "name": "",
            "type": "bytes4"
        }],
        "name": "supportsInterface",
        "outputs": [{
            "internalType": "bool",
            "name": "",
            "type": "bool"
        }],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }]

# sourcery skip: avoid-builtin-shadow
contract = get_contract(archivenode_url, "0x28729369d337861D6470db92a752b4835626DF99")
type = get_erc_type(contract)
print(type)