from ethpm import contract
from panoramix.decompiler import Decompilation
from web3 import Web3
from panoramix import decompiler
import requests

archivenode_url = 'https://api.archivenode.io/cbeed902-5bf9-44ca-9e31-9e9a58cf0c4e'
web3 = Web3(Web3.HTTPProvider(archivenode_url))

abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"ApprovalToCurrentOwner","type":"error"},{"inputs":[],"name":"ApproveToCaller","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"approved","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"HITLIST_SALE_PRICE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_HITLIST_MINT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_PUBLIC_MINT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PUBLIC_SALE_PRICE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMerkleRoot","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"},{"internalType":"uint256","name":"_quantity","type":"uint256"}],"name":"hitlistMint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"hitlistSale","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isRevealed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_quantity","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"placeholderTokenUri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"publicSale","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_merkleRoot","type":"bytes32"}],"name":"setMerkleRoot","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_placeholderTokenUri","type":"string"}],"name":"setPlaceHolderUri","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_baseTokenUri","type":"string"}],"name":"setTokenUri","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"teamMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"teamMinted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"togglePause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"togglePublicSale","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"toggleReveal","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"togglehitlistSale","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"totalHitlistMint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"totalPublicMint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"walletOf","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]
address = "0xd4f11c30078d352354c0b17eaa8076c825416493"
checksum_address = Web3.toChecksumAddress(address)


isConnected = web3.isConnected()
blocknumber = web3.eth.blockNumber
print("blocknumber=",blocknumber)

contract = web3.eth.contract(address=checksum_address, abi=abi)
print("name= ", contract.functions.name().call())
print("balanceOf=", contract.functions.balanceOf(Web3.toChecksumAddress("0x2A081F6473BcfB8ab3D4Fa25296B9f79CDD7503C")).call())
print("owner=", contract.functions.owner().call())
print("placeholderTokenUri=", contract.functions.placeholderTokenUri().call())
print("HITLIST_SALE_PRICE=", contract.functions.HITLIST_SALE_PRICE().call())
print("MAX_HITLIST_MINT=", contract.functions.MAX_HITLIST_MINT().call())
print("MAX_PUBLIC_MINT=", contract.functions.MAX_PUBLIC_MINT().call())
print("MAX_SUPPLY=", contract.functions.MAX_SUPPLY().call())
print("PUBLIC_SALE_PRICE=", contract.functions.PUBLIC_SALE_PRICE().call())
print("totalSupply=", contract.functions.totalSupply().call())
print("symbol=", contract.functions.symbol().call())
# print("decimals=", contract.functions.decimals().call())

block =  web3.eth.get_block("latest")
print("block=",block)


balance = web3.eth.getBalance('0xa41F142b6eb2b164f8164CAE0716892Ce02f311f')
print('Connected: ', isConnected, 'BlockNumber: ', blocknumber, 'Account Balance: ', (web3.fromWei(balance, 'Ether')))

transaction = web3.eth.get_transaction('0x5798fbc45e3b63832abc4984b0f3574a13545f415dd672cd8540cd71f735db56')
print("transaction=",transaction)

result1 = web3.eth.get_code('0x6C8f2A135f6ed072DE4503Bd7C4999a1a17F824B')
print("result1-contract address=",result1)
if result1 == b'':
    print("1 NOT  contract address")
else:
    print("1 YES contract address")

result2 = web3.eth.get_code('0xd3CdA913deB6f67967B99D67aCDFa1712C293601')
print("result2-non contract address=",result2)
if result2 == b'':
    print("2 NOT  contract address")
else:
    print("2 YES contract address")


# https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API#get-token-info
ethplorer_url = 'https://api.ethplorer.io'
ethplorer_api = "EK-rM3jG-us92oy1-QLLsQ"
token_info= requests.get(ethplorer_url+'/getTokenInfo/'+'0xf3db5fa2c66b7af3eb0c0b782510816cbe4813b8?apiKey='+ethplorer_api)
print("token_info=",token_info)
print("token content =",token_info.content)

log = requests.get("https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=0&toBlock=latest&address=0xd4f11C30078d352354c0B17eAA8076C825416493&apikey=D2AZWJH4VJNNYRH88WA91YZ2KM62N4EIDX")
                   "https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=0&toBlock=latest&address=0xd4f11C30078d352354c0B17eAA8076C825416493S&apikey=D2AZWJH4VJNNYRH88WA91YZ2KM62N4EIDX"
print("log=",log)



