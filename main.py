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

def proces_noaa_nbm_data(date, model, fxx, product):
    l = Ledger(f'NOAA_NBM_{date}_{model}_{fxx}_{product}')
    l.log_start()
    
    try:
        h = Herb(date, model, fxx, product)
        l.log_message('Downloaded data')
    except Exception as e:
        l.log_error(e)
        l.log_end()
        return
    try:
        h.save_file()
        l.log_message('Saved data')
    except Exception as e:
        l.log_error(e)
        l.log_end()
        return

    try:
        path = h.generate_file_path()
        s = Storage()
        s.upload_file(path)
        l.log_message('Uploaded data')
    except Exception as e:
        l.log_error(e)
        l.log_end()
        return