## SCA - Smart Contract Analyzer
From the user get contract address to retrieve one record from Etherscan.


**Token Transfers for a Contract**

The bigquery-public-data.crypto_ethereum.token_transfers has all the ERC20 token 
transfers in Ethereum. Use the bigquery-public-data.crypto_ethereum.contracts.address and
join it with bigquery-public-data.crypto_ethereum.token_transfers.from_address and 
bigquery-public-data.crypto_ethereum.token_transfers.to_address to find all the token 
transfers for the bigquery-public-data.crypto_ethereum.contracts.address. 
This table contains ONLY ERC20 token transfers. 


**Token details for the Contract**
Use the above bigquery-public-data.crypto_ethereum.token_transfers.token_address to get all the 
token details. The token_address is the address of the contract where the token 
developer created the contract with maximum number of tokens and other data. 
The token can be transferred to other contract or to an individual (EOA)

**Transactions for a Contract**

For each row from bigquery-public-data.crypto_ethereum.token_transfers, find 
bigquery-public-data.crypto_ethereum.token_transfers.transaction_hash and go to 
bigquery-public-data.crypto_ethereum.transactions to find all the transactions associated with that contract.
The bigquery-public-data.crypto_ethereum.token_transfers.token_address is the token contract address

**Logs for a Contract**

Use bigquery-public-data.crypto_ethereum.transactions.transaction_hash to find all the logs
for the contract from bigquery-public-data.crypto_ethereum.logs

**Traces for a Contract**

Use bigquery-public-data.crypto_ethereum.transactions.transaction_hash to find all the internal transactions 
for the contract bigquery-public-data.crypto_ethereum.traces

## Find Customers
From all the transactions found above, use bigquery-public-data.crypto_ethereum.transactions.from_address and
bigquery-public-data.crypto_ethereum.transactions.to_address not equal to 
bigquery-public-data.crypto_ethereum.contracts.address are all customers.

**Big Query setup in GCP console**

Use API & Services/Create Credentials to create service account and add bigquery roles

# Examples
## 1. Developer D created new Contract C

Developer D deployed contract C creates a row in crypto_ethereum.transactions 
with from_address=D's account address, to_address=null contract C's new address and
receipt_contract_address = Contract address of C. If
contract has 20 tokens all those token initial address will be same as 
C's new address.

## 2. Person X sends ether to Contract C
For the contract C created above, person X sent ether to transfer one token. After
the transaction, it will have from_address = Contract C address
to_address = Person X address and receipt_contract_address = null

## 3. Contract C sends ether to Contract D

## 4. Person X sends ether to Person Y

## Type of Transactions
- From EOA to EOA (Person to Person transfer)
- From EOA to Contract Creation
- From EOA to Contract Execution
- From Contract to Contract Creation
- From Contract to Contract Execution

## Sample Transaction
1 Ether = 10^18 wei
1 gwei = 10^-9 ETH
{
   "value":"0", (wei)
   "gas":"4197250", (wei) A gas limit, max amount gas this transaction can use. For
   simple txn it is 21000
   "gasPrice":"36955980105", (in wei, how much we're willing to pay) 

   "cumulativeGasUsed":"19035965",
   "gasUsed":"4197250", (actual amount of gas used for the transaction in wei)

# SCA - EOA Analyzer
Wallet Analyzer analyzes EOA address to retrieve all the transactions, for each transaction
identifies if to_address is contract or another EOA. If it is contract, retrieves ABI
and use the SCA - Smart Contract Analyzer to perform analytic. For this to work we need
user's read-only permission to access the wallet data.


# UI Wallet Address Retrieval
When user interacts with wallet, use the Javascript to retrieve store data in the
sca. From this data, identify the user wallet public address, token info etc.,
and use it to run the SCA to perform analytic.