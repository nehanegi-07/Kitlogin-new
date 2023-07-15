--get tokens for a contract address is retrieved from get_token_transfers.sql
SELECT * FROM bigquery-public-data.crypto_ethereum.tokens  where address in
('0xdac17f958d2ee523a2206206994597c13d831ec7',
'0xdac17f958d2ee523a2206206994597c13d831ec7',
'0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
)