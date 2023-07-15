--get all logs for the contract
SELECT * FROM bigquery-public-data.crypto_ethereum.logs as log where DATE(log.block_timestamp) >= "2021-12-16" and log.transaction_hash in
(SELECT transaction_hash FROM bigquery-public-data.crypto_ethereum.token_transfers  as tc_tran WHERE DATE(tc_tran.block_timestamp) >= "2021-12-16"  and
tc_tran.from_address='0xa41f142b6eb2b164f8164cae0716892ce02f311f' or tc_tran.to_address='0xa41f142b6eb2b164f8164cae0716892ce02f311f')