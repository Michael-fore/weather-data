from herbie import Herbie
import pandas as pd
from pathlib import Path   
#co is CONUS
# main thing need to cosider is not duplicating  data here
# there are a BUNCH of  forecasts  and it is a TON of dataa

# H = Herbie("2022-04-01", model='nbm', fxx=10,  product='co', save_dir ='tmp' )

# ds = H.xarray()

# # print(ds[0].data_vars)

# dfs = [d.to_dataframe() for d in ds]
# # print(dfs[0].head())
# # [print(df.head()) for df in dfs]s

# index_cols = ['latitude', 'longitude', 'valid_time', 'time', 'step']

# [df.set_index(index_cols, inplace=True) for df in dfs]
# [print(df.head()) for df in dfs]
# [df.to_csv(f'tmp/{i}.csv') for i, df in enumerate(dfs)]

# master_df =  pd.concat(dfs, axis=1)
# print(master_df.head())

# master_df.to_csv('tmp/nbm_2022-04-01_10_co.csv')

class Herb:
    def __init__(self, date, model, fxx, product, save_dir='tmp'):
        self.date = date
        self.model = model
        self.fxx = fxx
        self.product = product
        self.save_dir = save_dir
        self.h = Herbie(date, model=model, fxx=fxx, product=product, save_dir=save_dir)

        if not self.h:
            self.h.download()
        # self.h.download()

    def save_file(self):

      self.make_master_dataframe().to_csv(self.generate_file_path())
      

    def generate_file_path(self):
        year, month, day = self.date.split('-')
        path =  f'{self.save_dir}/{self.model}/{year}/{month}/{day}/{self.fxx}/'
        Path(path).mkdir(parents=True, exist_ok=True)
        path += f'{self.product}.csv'
        return path

    def make_master_dataframe(self):
        master_df = pd.DataFrame()
        #since these datasets are big, should chunck it up
        # as much as possible
        for i, df in enumerate(self.make_data_frames()):
            # print(df.head().to_string())
            # print(master_df.head().to_string())
            print('Loading DS: ', i)
            print(master_df.columns)
            try:
                print(f'Loading {len(df)} rows into master_df which has {len(master_df)} rows') 
                master_df = pd.concat([master_df, df], axis=1)
            except pd.errors.InvalidIndexError:
                #rename incoming columns
                print('errors on ds', i)
                # print(df.columns)
                # df.to_csv(f'tmp/{i}.csv')

                # df.columns = [f'{col}_{i}_ix' for ix, col in enumerate(df.columns)]
                # df[df.duplicated(keep=False)].head(100).to_csv(f'tmp/___dupes_{i}.csv')
                # print(df.index.duplicated(keep=False))#.to_csv(f'tmp/__dupes_{i}.csv')
                # dupe_df.to_csv(f'tmp/{i}.csv')
                # print()
                # master_df = pd.concat([master_df, df], axis=1)
        return master_df
    
    def make_data_frames(self):
        '''
        Could use a generator here, actually, maybe i will
        '''
        # ds = self.h.xarray()
        # dfs = [d.to_dataframe() for d in ds]
        # index_cols = ['latitude', 'longitude', 'valid_time', 'time', 'step']
        # [df.set_index(index_cols, inplace=True) for df in dfs]
        # return dfs
        ds = self.h.xarray()
        for df in ds:
            df = df.to_dataframe()
            df = self.clean_dataframe_col(df)
            #need to study other grib systems, this is hardcoded for nbm atm
            yield df.set_index(['latitude', 'longitude', 'valid_time', 'time', 'step'])

    def clean_dataframe_col(self, df):
        DROP_COLS = ['unknown','gribfile_projection']
        df.drop(columns=DROP_COLS, inplace=True, errors='ignore')
        return df
    

date, fxx, model, product = '2022-04-01', 10,  'nbm', 'co'
h = Herb(date, model, fxx, product)
h.save_file()
# s = Storage()
path = h.generate_file_path()
# s.upload_file(path)
print(path)