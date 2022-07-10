import logging
from datetime import datetime
from random import randint, random

import pandas as pd
import pytz
from arch import arch_model
from arch.univariate import ARX
from django_pandas.io import read_frame
from pmdarima import ARIMA, auto_arima
from pmdarima.arima import ADFTest
from pmdarima.metrics import smape
from pmdarima.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.ar_model import AR

from .alphavantage import SYMBOLS
from .models import Ticker

logger = logging.getLogger(__name__)


def test_model():
    logger.info('Loading data...')
    df = read_frame(
        Ticker.objects.all(),
        index_col='tick_at', datetime_index=True)
    df['price'] = df['xmr'] / df['btc']
    y_train, y_test = train_test_split(df['price'])
    arima = train_arima(y_train)
    garch = train_garch(arima.arima_res_.resid)

    logger.info(f'Testing model on {len(y_test)}...')
    forecasts = []
    logger.info(f'From {y_test.index[0]} to {y_test.index[-1]}')
    for ix, val in y_test.items():
        fc = next_forecast(arima, garch, ix, val)
        forecasts.append(fc)

    logger.info(f'Arima order: {arima.order}')
    mse = mean_squared_error(y_test, forecasts)
    logger.info(f'Mean squared error: {mse:.6f}')
    smape_score = smape(y_test, forecasts)
    logger.info(f'sMAPE: {smape_score:.2f}')


def predict_btc_100():
    logger.info('Loading data...')
    df = read_frame(
        Ticker.objects.all(),
        index_col='tick_at', datetime_index=True)
    # y_train, y_test = train_test_split(df['btc'])
    y_train = df['btc']

    # test stationary
    adf_test = ADFTest(alpha=0.05)
    adf_res = adf_test.should_diff(y_train)
    logger.info(f'adf test: {adf_res}')

    arima = train_arima(y_train)
    # garch = train_garch(arima.arima_res_.resid)

    days = (datetime(2023, 1, 1, tzinfo=pytz.UTC) - df['btc'].index[-1]).days
    pred = arima.predict(n_periods=days, return_conf_int=False)
    mu = pred[0]


def next_forecast(arima: ARIMA, garch, dt: datetime, actual: float) -> float:
    mu = arima.predict(n_periods=1, return_conf_int=False).tolist()[0]
    et = garch.forecast(params=None, horizon=1).mean['h.1'].iloc[-1]
    garch.update(mu)
    Ticker.objects.filter(tick_at=dt).update(arima=mu, garch=et)
    arima.update(actual)
    return val


def train_arima(y_train) -> ARIMA:
    logger.info(f'Training arima model on {len(y_train)}...')
    arima = auto_arima(y_train, seasonal=False)
    return arima


def train_garch(residuals):
    dict_aic = {}

    for l in range(5):
        for p in range(1, 5):
            for q in range(1, 5):
                model = arch_model(residuals, mean='ARX', lags=l, vol='GARCH', p=p, o=0, q=q, dist='normal', rescale=True)
                res = model.fit()
                dict_aic[(l, p, q)] = res.aic

    df_aic = pd.DataFrame.from_dict(dict_aic, orient='index', columns=['aic'])
    l, p, q = df_aic[df_aic.aic == df_aic.aic.min()].index[0]
    logger.info(f'ARIMA-GARCH order is ({l}, {p}, {q})')
    final_model = arch_model(residuals, mean='ARX', lags=l, vol='GARCH', p=p, o=0, q=q, dist='normal', rescale=True).fit()
    return final_model


def grid_search_buy_sell():
    logger.info(f'Grid search buy and sell')
    # usdt_perc 0.05 = 14418
    # usdt_perc 0.04 = 15487
    # usdt_perc 0.03 = 16789
    # usdt_perc 0.02 = 18213
    # usdt_perc 0.01 = 19734
    # usdt_perc 0.0075 = 20481
    # usdt_perc 0.0050 = 20601
    # usdt_perc 0.0025 = 19707
    # usdt_perc 0.001 = 18888
    # left usdt_perc at 1%
    # usdt_perc = 0.01

    # signal
    # 10 = 19858
    # 25 = 19859
    # 50 = 19734
    # 75 = 19647
    # 100 = 19637
    # signal = 25

    # base
    # 50 = 19965
    # 75 = 20740
    # 100 = 19847
    # 150 = 19657
    # 200 = 19859
    # base = 75

    # usdt_perc
    # 08 = 20688
    # 09 = 20541
    # 10 = 20740
    # 11 = 21625
    # 12 = 21640
    perc = 0.012

    # signal
    # 10 = 21387
    # 20 = 21465
    # 30 = 21751
    # 40 = 21553
    # 50 = 21455
    signal = 30

    # base
    # 50 = 21454
    # 60 = 21868
    # 70 = 21609
    # 80 = 21828
    # 90 = 21061
    base = 80

    param_groups = [
        {'signal': signal, 'base': base, 'perc': perc},
    ]
    results = {}
    for params in param_groups:
        balance = buy_sell(**params)
        results[balance] = params
    for k, v in results.items():
        logger.info(f'Balance {k:.0f} params = {v}')


def buy_sell(signal, base, perc):
    df = read_frame(
        Ticker.objects.all(),
        index_col='tick_at', datetime_index=True)
    df['signal'] = df['btc'].rolling(signal).mean()
    df['base'] = df['btc'].rolling(base).mean()
    usdt = 11_000
    btc = usdt / df.iloc[0].btc
    for day, ticker in df.iterrows():
        if pd.isna(ticker.signal) or pd.isna(ticker.base):
            continue

        if day.day_of_week != 0:
            continue

        # sell when green
        if ticker.signal > ticker.base:
            action = 'sell'
            portion_btc = btc * perc
            portion = portion_btc * ticker.btc
            if portion > 50:
                btc -= portion_btc
                usdt += portion
            else:
                portion = 0

        # buy when red
        else:
            action = 'buy'
            portion = usdt * perc
            if portion > 50:
                usdt -= portion
                btc += portion / ticker.btc
            else:
                portion = 0

        total = usdt + btc * ticker.btc
        logger.info(f'{day} {action} {portion:.0f}: {total:.0f} [USDT {usdt:.0f} BTC {btc * ticker.btc:.0f}]')
    return total


def grid_search_buy_sell_ewm():
    logger.info(f'Grid search buy and sell')

    # perc 013 = 39914
    # signal 40 = 40293
    # base 90 = 40883
    # signal 85 = 43,373
    # base 260 = 48813
    # perc 019 = 50157
    # signal 105 = 51360

    # xmr added
    # signal 150 = 56333
    # base 290 = 56333
    # perc = 019

    perc = 0.019
    # signal = 150  # 50,364
    # added XMR = 36,644
    # investment 5k * 3 = 36,644
    # added ETH = 7,015
    signal = 10  # 31,018
    base = 70  # 104%

    param_groups = [
        # {'signal': signal, 'base': base, 'perc': perc},
        {'signal': signal, 'base': base, 'perc': 0.007},
        {'signal': signal, 'base': base, 'perc': 0.009},
        {'signal': signal, 'base': base, 'perc': 0.011},
        {'signal': signal, 'base': base, 'perc': 0.013},
        {'signal': signal, 'base': base, 'perc': 0.015},
    ]
    results = {}
    for params in param_groups:
        balance = buy_sell_ewm(**params)
        results[balance] = params
    for k, v in results.items():
        logger.info(f'ROI {(k-20_000)/200:.0f}%  Balance {k:.0f}  Params = {v}')


def buy_sell_ewm(signal, base, perc):
    df = read_frame(
        Ticker.objects.all(),
        index_col='tick_at', datetime_index=True)
    lower_symbols = [s.lower() for s in SYMBOLS]
    balances = {
        'usdt': 5_000,
    }
    for symbol in lower_symbols:
        df[f'signal_{symbol}'] = df[symbol].ewm(signal).mean()
        df[f'base_{symbol}'] = df[symbol].ewm(base).mean()
        balances[symbol] = balances['usdt'] / df.iloc[0][symbol]
    for day, ticker in df.iterrows():
        if day.day_of_week != 0:
            continue

        logs = {}
        for symbol in lower_symbols:
            # skip if no averages
            if pd.isna(ticker[f'base_{symbol}']):
                continue

            # sell when green
            if ticker[f'signal_{symbol}'] > ticker[f'base_{symbol}']:
                portion_coin = balances[symbol] * perc
                portion_usd = portion_coin * ticker[symbol]
                if portion_usd > 50 and balances[symbol] > portion_coin:
                    balances[symbol] -= portion_coin
                    balances['usdt'] += portion_usd
                    logger.debug(f'Selling {symbol} of {portion_usd}')
            # buy when red
            else:
                portion_usd = balances['usdt'] * perc
                if portion_usd > 50 and balances['usdt'] > portion_usd:
                    balances['usdt'] -= portion_usd
                    balances[symbol] += portion_usd / ticker[symbol]
                    logger.debug(f'Buying {symbol} of {portion_usd}')
            logs[symbol] = balances[symbol] * ticker[symbol]

        total = sum(logs.values())
        logger.info(f'{day}  {total:.0f}  [{logs}]')
    return total + random()
