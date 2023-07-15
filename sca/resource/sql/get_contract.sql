--get contract data
SELECT * FROM bigquery-public-data.crypto_ethereum.contracts where address='0xa41f142b6eb2b164f8164cae0716892ce02f311f' and
date(block_timestamp) = '2021-12-16'