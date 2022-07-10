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
        sleep(12)

    # update db
    exists = 0
    for ts in data[SYMBOL_BTC]:
        btc_data = data[SYMBOL_BTC][ts]
        xmr_data = data[SYMBOL_XMR][ts]
        eth_data = data[SYMBOL_ETH][ts]
        bnb_data = data[SYMBOL_BNB][ts]
        ada_data = data[SYMBOL_ADA][ts]
        # sol_data = data[SYMBOL_SOL][ts]
        doge_data = data[SYMBOL_DOGE][ts]
        # dot_data = data[SYMBOL_DOT][ts]
        trx_data = data[SYMBOL_TRX][ts]
        # avax_data = data[SYMBOL_AVAX][ts]
        matic_data = data[SYMBOL_MATIC][ts]
        # uni_data = data[SYMBOL_UNI][ts]
        ltc_data = data[SYMBOL_LTC][ts]
        # ftt_data = data[SYMBOL_FTT][ts]
        link_data = data[SYMBOL_LINK][ts]
        xlm_data = data[SYMBOL_XLM][ts]
        # cro_data = data[SYMBOL_CRO][ts]
        algo_data = data[SYMBOL_ALGO][ts]
        atom_data = data[SYMBOL_ATOM][ts]
        # bch_data = data[SYMBOL_BCH][ts]
        etc_data = data[SYMBOL_ETC][ts]
        vet_data = data[SYMBOL_VET][ts]
        # mana_data = data[SYMBOL_MANA][ts]
        # flow_data = data[SYMBOL_FLOW][ts]
        hbar_data = data[SYMBOL_HBAR][ts]
        theta_data = data[SYMBOL_THETA][ts]
        eos_data = data[SYMBOL_EOS][ts]
        zec_data = data[SYMBOL_ZEC][ts]

        date = make_aware(datetime.strptime(ts, '%Y-%m-%d'))
        ticker, created = Ticker.objects.update_or_create(
            tick_at=date,
            defaults={
                'btc': float(btc_data['4a. close (USD)']),
                'xmr': float(xmr_data['4a. close (USD)']),
                'eth': float(eth_data['4a. close (USD)']),
                'bnb': float(bnb_data['4a. close (USD)']),
                'ada': float(ada_data['4a. close (USD)']),
                # 'sol': float(sol_data['4a. close (USD)']),
                'doge': float(doge_data['4a. close (USD)']),
                # 'dot': float(dot_data['4a. close (USD)']),
                'trx': float(trx_data['4a. close (USD)']),
                # 'avax': float(avax_data['4a. close (USD)']),
                'matic': float(matic_data['4a. close (USD)']),
                # 'uni': float(uni_data['4a. close (USD)']),
                'ltc': float(ltc_data['4a. close (USD)']),
                # 'ftt': float(ftt_data['4a. close (USD)']),
                'link': float(link_data['4a. close (USD)']),
                'xlm': float(xlm_data['4a. close (USD)']),
                # 'cro': float(cro_data['4a. close (USD)']),
                'algo': float(algo_data['4a. close (USD)']),
                'atom': float(atom_data['4a. close (USD)']),
                # 'bch': float(bch_data['4a. close (USD)']),
                'etc': float(etc_data['4a. close (USD)']),
                'vet': float(vet_data['4a. close (USD)']),
                'hbar': float(hbar_data['4a. close (USD)']),
                'theta': float(theta_data['4a. close (USD)']),
                'eos': float(eos_data['4a. close (USD)']),
                'zec': float(zec_data['4a. close (USD)']),
            }
        )
        logger.info(f'Saved {ticker}')
        exists += int(not created)
        if exists >= 3:
            break
