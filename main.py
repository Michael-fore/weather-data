import functions_framework
import requests
from main_nbm import process_noaa_nbm_data


#once i get the needed funcitonality figured out
# genercize this to w wrapper that wraps the main functionn and cna genereate needed metadata

@functions_framework.http
def proces_noaa_nbm_data(request:requests.Request):
    '''
    proces_noaa_nbm_data(date, model, fxx, product):

    gcloud functions deploy python-http-function \
        --gen2 \
        --runtime=python312 \
        --region=us-central1 \
        --source=gcp_funcs.py    \
        --entry-point=proces_noaa_nbm_data \
        --trigger-http \
        --allow-unauthenticated
        
    test url:
    https://us-central1-data-bridge-338204.cloudfunctions.net/noaa-nbm-nbs?date=2022-01-01&model=nbm&fxx=1&product=co
    '''

    kwarg_list = ['date', 'model', 'fxx', 'product']
    for kwarg in kwarg_list:
        if kwarg not in request.args:
            print(f'Error: {kwarg} is a required argument')
            return 'And you may ask yourself, "Well, how did I get here?" .. Letting the days go by, let the water hold me down'

    date, model, fxx, product = request.args['date'], request.args['model'], request.args['fxx'], request.args['product']

    return process_noaa_nbm_data(date, model, fxx, product)
