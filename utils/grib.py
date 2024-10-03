# blend.t01z.core.f001.ak.grib2     
from cfgrib.xarray_store import open_variable_datasets,merge_datasets
import xarray as xr
import io
import cfgrib
# cloud run lets you write to the /tmp file, 
# 


ds = cfgrib.open_datasets('local/data/blend.t00z.master.f001.co.grib2')

print(ds)