import logging
from datetime import datetime
from time import sleep

import requests
from django.utils.timezone import make_aware

from main.models import Ticker

API_KEY = 'OTFF029ZC651LYCP'
HOST = 'https://www.alphavantage.co'
SYMBOL_BTC = 'BTC'
SYMBOL_XMR = 'XMR'
SYMBOL_ETH = 'ETH'
SYMBOL_BNB = 'BNB'
SYMBOL_ADA = 'ADA'
SYMBOL_SOL = 'SOL'
SYMBOL_DOGE = 'DOGE'
SYMBOL_DOT = 'DOT'
SYMBOL_TRX = 'TRX'
SYMBOL_AVAX = 'AVAX'
SYMBOL_MATIC = 'MATIC'
SYMBOL_UNI = 'UNI'
SYMBOL_LTC = 'LTC'
SYMBOL_FTT = 'FTT'
SYMBOL_LINK = 'LINK'
SYMBOL_XLM = 'XLM'
SYMBOL_CRO = 'CRO'
SYMBOL_ALGO = 'ALGO'
SYMBOL_ATOM = 'ATOM'
SYMBOL_BCH = 'BCH'
SYMBOL_ETC = 'ETC'
SYMBOL_VET = 'VET'
SYMBOL_MANA = 'MANA'
SYMBOL_FLOW = 'FLOW'
SYMBOL_HBAR = 'HBAR'
SYMBOL_THETA = 'THETA'
SYMBOL_EOS = 'EOS'
SYMBOL_ZEC = 'ZEC'
SYMBOL_HT = 'HT'
# SYMBOL_AC = 'AC'

SYMBOLS = [
    SYMBOL_BTC, SYMBOL_XMR, SYMBOL_ETH,
    SYMBOL_BNB, SYMBOL_ADA, SYMBOL_DOGE,
    SYMBOL_TRX, SYMBOL_MATIC, SYMBOL_LTC,
    SYMBOL_LINK, SYMBOL_XLM, SYMBOL_ALGO,
    SYMBOL_ATOM, SYMBOL_ETC, SYMBOL_VET,
    SYMBOL_HBAR, SYMBOL_THETA, SYMBOL_EOS,
    SYMBOL_ZEC,
]

logger = logging.getLogger(__name__)


def get_data(delta=True):
    logger.info('Getting alphavantage data...')

    # fetch raw data
    data = {}
    for symbol in reversed(SYMBOLS):
        params = {
            'function': 'DIGITAL_CURRENCY_DAILY',
            'symbol': symbol,
            'market': 'USD',
            'interval': '1DAY',
            # 'outputsize': 'compact' if delta else 'full',
            'apikey': API_KEY,
        }
        logger.info(f'Fetching {symbol}...')
        res = requests.get(f'{HOST}/query', params=params)
        res.raise_for_status()
        res_data = res.json()
        data[symbol] = res_data['Time Series (Digital Currency Daily)']
        if len(data[symbol]) < 1_000:
            raise ValueError(f'Expected 1k data items but only found {len(data[symbol])} for {symbol}')
        sleep(12)

    # update db
    exists = 0
    for ts in data[SYMBOL_BTC]:
        defaults = {s.lower(): float(data[s][ts]['4a. close (USD)']) for s in SYMBOLS}

        date = make_aware(datetime.strptime(ts, '%Y-%m-%d'))
        ticker, created = Ticker.objects.update_or_create(
            tick_at=date,
            defaults=defaults
        )
        logger.info(f'Saved {ticker}')
        exists += int(not created)
        if delta and exists >= 3:
            break
