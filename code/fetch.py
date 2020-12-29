import pandas as pd
import os
from datetime import datetime, date, timedelta
import numpy as np

__author__ = 'Duy Cao'
__copyright__ = 'Duy Cao, 2020'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/bitcoin-indicated'
__version__ = '1.0'

NOMICS_API_KEY = 'e19a802cb19367a00e3d66638e9e974f'

def live_data():
    # Read historical exchange rate from Nomics
    nomics_url = f'https://api.nomics.com/v1/exchange-rates/history?key={NOMICS_API_KEY}&start=2020-01-01T00%3A00%3A00Z&currency=BTC'
    nomics_df = pd.read_json(nomics_url)
    nomics_df['timestamp'] = nomics_df['timestamp'].dt.date
    nomics_df = nomics_df.rename(columns={'timestamp':'date', 'rate':'nomics'})
    latest_date = nomics_df['date'].max()

    # Read historical exchange rate from Coindesk
    coindesk_url = f'https://api.coindesk.com/v1/bpi/historical/close.json?start=2020-01-01&end={latest_date}'
    df = pd.read_json(coindesk_url)
    df = df.drop(['disclaimer', 'time'], 1)
    df = df[:-2].reset_index().rename(columns={'index':'date', 'bpi':'coindesk'})
    df['date'] = pd.to_datetime(df['date']).dt.date

    df = df.merge(nomics_df, on=['date'], how='inner')

    return df
