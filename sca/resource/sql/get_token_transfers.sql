SELECT
  --get contract data, one row
  con.address as con_address,
  con.bytecode as con_bytecode,
  con.function_sighashes as con_function_sighashes,
  con.is_erc20 as con_is_erc20,
  con.is_erc721 as con_is_erc721,
  con.block_timestamp as con_block_timestamp,
  con.block_number con_block_no,
  con.block_hash as con_block_hash,
  --get all the token transfer data for the con_address, multiple rows
  tk_tran.token_address as tk_tran_token_address,
  tk_tran.from_address,
  tk_tran.to_address,
  tk_tran.transaction_hash,
  tk_tran.log_index,
  tk_tran.value as tk_trans_value,
  tk_tran.transaction_hash as tk_transaction_hash,

FROM
  bigquery-public-data.crypto_ethereum.contracts AS con
LEFT JOIN
  bigquery-public-data.crypto_ethereum.token_transfers AS tk_tran
ON
  con.address = tk_tran.token_address AND
  con.block_timestamp  =tk_tran.block_timestamp

WHERE
  DATE(con.block_timestamp) = '2021-12-16'
  AND con.address='0xa41f142b6eb2b164f8164cae0716892ce02f311f'