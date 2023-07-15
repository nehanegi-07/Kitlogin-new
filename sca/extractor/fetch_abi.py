
import requests
import json
from web3 import Web3
from web3 import contract

# Exports contract ABI in JSON

ETHERSCAN_ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&action=getabi&address='
archivenode_url = 'https://api.archivenode.io/cbeed902-5bf9-44ca-9e31-9e9a58cf0c4e'

https://api.etherscan.io/api
   ?module=transaction
   &action=getstatus
   &txhash=0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a
   &apikey=YourApiKeyToken

def get_abi(address):

    assert address is not None
    response = requests.get('%s%s'%(ETHERSCAN_ABI_ENDPOINT, address))
    response_json = response.json()
    abi_json = json.loads(response_json['result'])
    result = json.dumps({"abi":abi_json}, indent=4, sort_keys=True)
    print("result=",result)


get_abi("0x7a250d5630b4cf539739df2c5dacb4c659f2488d")

w3 = Web3(Web3.HTTPProvider(archivenode_url))


mkr_contract_address = '0xe66b31678d6c16e9ebf358268a790b763c133750'
address2 = Web3.toChecksumAddress(mkr_contract_address)

abi = '[{"inputs":[{"internalType":"contract IZeroEx","name":"zeroEx","type":"address"},{"internalType":"address payable","name":"allowanceTarget","type":"address"},{"internalType":"address payable","name":"beneficiary","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"allowanceTarget","type":"address"}],"name":"AllowanceTargetChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beneficiary","type":"address"}],"name":"BeneficiaryChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes4","name":"signature","type":"bytes4"},{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"ImplementationOverrideSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"zeroEx","type":"address"}],"name":"ZeroExChanged","type":"event"},{"inputs":[],"name":"getAllowanceTarget","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBeneficiary","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"signature","type":"bytes4"}],"name":"getFunctionImplementation","outputs":[{"internalType":"address","name":"impl","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getZeroEx","outputs":[{"internalType":"contract IZeroEx","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"msgData","type":"bytes"},{"internalType":"address","name":"feeToken","type":"address"},{"internalType":"uint256","name":"fee","type":"uint256"}],"name":"optimalSwap","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"msgData","type":"bytes"},{"internalType":"address","name":"feeToken","type":"address"},{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"uint256","name":"inputAmount","type":"uint256"},{"internalType":"address","name":"outputToken","type":"address"},{"internalType":"uint256","name":"fee","type":"uint256"}],"name":"proxiedSwap","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"newAllowanceTarget","type":"address"}],"name":"setAllowanceTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"beneficiary","type":"address"}],"name":"setBeneficiary","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"signature","type":"bytes4"},{"internalType":"address","name":"implementation","type":"address"}],"name":"setImplementationOverride","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IZeroEx","name":"newZeroEx","type":"address"}],"name":"setZeroEx","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

tx_hash = '0x9eb2d5ac729c221e47e980051934047c46aca2bacb2e40e6f79859c5b624b065'
transaction = w3.eth.getTransaction(tx_hash)
mkr_contract = w3.eth.contract(address=address2, abi=abi)
print(mkr_contract.decode_function_input(transaction.input))
