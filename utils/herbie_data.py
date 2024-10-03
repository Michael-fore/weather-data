from herbie import Herbie
import cfgrib
import requests
from pathlib import Path    
#co is CONUS
# main thing need to cosider is not duplicating  data here
# there are a BUNCH of  forecasts  and it is a TON of dataa

H = Herbie("2022-04-01", model='nbm', fxx=10,  product='co', save_dir ='tmp' )

ds = H.xarray()

# print(ds[0].data_vars)

dfs = [d.to_dataframe() for d in ds]
# print(dfs[0].head())
# [print(df.head()) for df in dfs]s

index_cols = ['latitude', 'longitude', 'valid_time', 'time', 'step']

[df.set_index(index_cols, inplace=True) for df in dfs]

master_df =     dfs[0].join(dfs[1:], suffixes=('', '_1'))
print(master_df.head())