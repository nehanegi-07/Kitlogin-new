import os
import pandas as pd


file = f"{os.getcwd()}/sca/resource/part-00000-d0ac02a5-d64a-429b-b929-f544c34bf3f7-c000.snappy.parquet"
# read paraquet file to df
df = pd.read_parquet(file)
print(df.head())

