from utils import Herb, Storage,  Ledger

#
# All the integration for the other data source should come togethere here
# Each fuction should be independatly callable are parallelizable
#

def try_except(func, l:Ledger):
    try:
        func()
    except Exception as e:
        l.log_error(e)
        l.log_end()

def process_noaa_nbm_data(date, model, fxx, product):
    l = Ledger(f'NOAA_NBM_{date}_{model}_{fxx}_{product}')
    l.log_start()
    
    h = Herb(date, model, fxx, product)
    l.log_message('Downloaded data')

    h.save_file()
    l.log_message('Saved data')
    l.log_error(e)
    l.log_end()

    path = h.generate_file_path()
    s = Storage()
    s.upload_file(path)
    l.log_message('Uploaded data')

    
if __name__ == '__main__':
    process_noaa_nbm_data('2024-06-01', 'nbm', 1, 'co')
