import matplotlib.pyplot as plt
from datetime import datetime

# Sample data
data_samples = [
    {
        "blockNumber": "16807996",
        "timeStamp": "1678576055",
        "hash": "0x54d353bca48f05e22be0320f9f2d8970b3451e17c636e35d6131220da0a3198e",
        "nonce": "6",
        "blockHash": "0xa045d646d4b713c6e9055b63d1795c9c26a75bf16185a8ba8a01648741e49dcb",
        "from": "0xc5374bca247f4d77273b96fcac058be760ebc6a3",
        "contractAddress": "0x4c3cfeb42aaea576ceada3e7498b2981a8e8b555",
        "to": "0x95ba4cf87d6723ad9c0db21737d862be80e93911",
        "value": "29655916115773925070530298846711",
        "tokenName": "USDC Inu",
        "tokenSymbol": "USDCINU",
        "tokenDecimal": "18",
        "transactionIndex": "3",
        "gas": "180371",
        "gasPrice": "35000000000",
        "gasUsed": "138186",
        "cumulativeGasUsed": "394927",
        "input": "deprecated",
        "confirmations": "389348"
    },
    {
        "blockNumber": "14919183",
        "timeStamp": "1654581151",
        "hash": "0xfb167fc2f797d43dcfba5f16764532756ccd5ad77f6d2e9ef4a9f5d597816a25",
        "from": "0x49b319849d2dbf56254155c9ceb46512b386dd25",
        "to": "0x95ba4cf87d6723ad9c0db21737d862be80e93911",
        "value": "574275922094568",
        "contractAddress": "",
        "input": "",
        "type": "call",
        "gas": "92894",
        "gasUsed": "0",
        "traceId": "0_0_0_0_0_0",
        "isError": "0",
        "errCode": ""
    },
    {
        "blockNumber": "16807946",
        "timeStamp": "1678575455",
        "hash": "0x74d6c2337bdb3a70259bb16d6f83a1b44bd4f0ea709576831ab382af9ef5da29",
        "nonce": "1",
        "blockHash": "0xb32d78b9e966975dde045a8c619dc77f5d057b09635a717aa06b540be9f90b4f",
        "transactionIndex": "1",
        "from": "0x09bba64db7df2fb5bb9a329dad4243153aedef61",
        "to": "0x95ba4cf87d6723ad9c0db21737d862be80e93911",
        "value": "0",
        "gas": "21000",
        "gasPrice": "45000000000",
        "isError": "0",
        "txreceipt_status": "1",
        "input": "0x",
        "contractAddress": "",
        "cumulativeGasUsed": "68150",
        "gasUsed": "21000",
        "confirmations": "389399",
        "methodId": "0x",
        "functionName": ""
    }
]

# Extract timestamps and convert them to datetime objects
timestamps = [datetime.fromtimestamp(int(data["timeStamp"])) for data in data_samples]

# Count the number of transactions per day
transactions_per_day = {}
for timestamp in timestamps:
    date = timestamp.date()
    if date in transactions_per_day:
        transactions_per_day[date] += 1
    else:
        transactions_per_day[date] = 1

# Sort the transactions by date
sorted_transactions = sorted(transactions_per_day.items())

# Extract the dates and transaction counts
dates = [date for date, _ in sorted_transactions]
transaction_counts = [count for _, count in sorted_transactions]

# Plotting the data
plt.figure(figsize=(12, 6))
plt.plot(dates, transaction_counts, marker='o')
plt.xlabel('Date')
plt.ylabel('Number of Transactions')
plt.title('Transaction Volume over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("tx_over_time.png")
