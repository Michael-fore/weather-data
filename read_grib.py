import xarray as xr


path = '/Users/skunkworks/Downloads/blend.t00z.master.f001.co.grib2'

ds_grib = xr.open_dataset(path, engine='cfgrib', filter_by_keys={'typeOfLevel': 'heightAboveGround'})

print(ds_grib)