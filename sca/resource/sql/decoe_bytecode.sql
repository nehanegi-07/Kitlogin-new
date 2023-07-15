-- Disassemble Contract bytecode
create temp function disassemble_bytecode(bytecode string)
returns array<struct<name string, fee int64, pushData string>>
language js as """
 return parseCode(bytecode);
 """
options (
 library="gs://ethereum-etl-bigquery/disassemble_bytecode.js"
);
select disassemble_bytecode(bytecode) as op
from `bigquery-public-data.crypto_ethereum.contracts`
where address = '0xa41f142b6eb2b164f8164cae0716892ce02f311f' and
date(block_timestamp) = '2021-12-16'