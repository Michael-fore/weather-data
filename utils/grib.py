# blend.t01z.core.f001.ak.grib2     

import xarray as xr

path=r'local\data\blend.t00z.master.f001.co.grib2'

ds = xr.load_dataset(path, engine='cfgrib')



# # convert file from bytes to text
# with open(path, 'rb') as f:
#     data = f.read()

# # print(data)
# with open(path+'.csv', 'w') as f:
#     f.write(data.decode('utf-8'))


# print(ds)
