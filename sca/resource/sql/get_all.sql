SELECT
  --get all transactions for the con_address, multiple rows
  tx.hash as tx_hash,
  tx.transaction_index,
  tx.value as tx_value,
  tx.gas as tx_gas,
  tx.gas_price as tx_gas_price,
  tx.input as tx_input,
  tx.receipt_cumulative_gas_used,
  tx.receipt_gas_used,
  tx.receipt_contract_address,
  tx.receipt_status,
  tx.max_fee_per_gas,
  tx.max_priority_fee_per_gas,
  tx.transaction_type,
  tx.receipt_effective_gas_price,
  tx.block_timestamp as tx_block_timestamp,
  --get all logs for all the transactions, multiple rows
  log.log_index,
  log.address,
  log.data,
  log.topics,
  --get all traces for all the transactions, multiple rows
  trc.from_address,
  trc.to_address,
  trc.value,
  trc.input,
  trc.output,
  trc.trace_type,
  trc.call_type,
  trc.reward_type,
  trc.gas_used as trc_gas_used,
  trc.gas as trc_gas,
  trc.subtraces
FROM
  bigquery-public-data.crypto_ethereum.transactions AS tx
LEFT JOIN
  bigquery-public-data.crypto_ethereum.logs AS log
ON
  tx.hash = log.transaction_hash AND
  tx.block_timestamp =log.block_timestamp
LEFT  JOIN
  bigquery-public-data.crypto_ethereum.traces AS trc
ON
  tx.hash = trc.transaction_hash AND
  tx.block_timestamp =trc.block_timestamp
WHERE
  (tx.from_address='0xa41f142b6eb2b164f8164cae0716892ce02f311f' OR
  tx.to_address= '0xa41f142b6eb2b164f8164cae0716892ce02f311f' OR
  tx.receipt_contract_address= '0xa41f142b6eb2b164f8164cae0716892ce02f311f') AND
  DATE(tx.block_timestamp) = '2021-12-16'