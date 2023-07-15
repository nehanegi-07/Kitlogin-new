--get transactions for all the token transfers for the contract
SELECT tx.hash, tx.transaction_index, tx.value, tx.gas, tx.gas_price, tx.input, tx.receipt_cumulative_gas_used,
tx.receipt_gas_used, tx.receipt_contract_address, tx.receipt_status, tx.max_fee_per_gas, tx.max_priority_fee_per_gas,
tx.transaction_type, tx.receipt_effective_gas_price
  FROM bigquery-public-data.crypto_ethereum.transactions as tx where tx.hash in
(SELECT transaction_hash FROM bigquery-public-data.crypto_ethereum.token_transfers  as
tc_tran WHERE DATE(tc_tran.block_timestamp) >= "2021-12-16"  and
tc_tran.from_address='0xa41f142b6eb2b164f8164cae0716892ce02f311f'
or tc_tran.to_address='0xa41f142b6eb2b164f8164cae0716892ce02f311f')
and DATE(tx.block_timestamp) >= "2021-12-16"