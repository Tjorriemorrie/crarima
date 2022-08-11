import logging
from collections import deque
from copy import deepcopy

import numpy as np
import pandas as pd
from cma import CMAOptions, CMAEvolutionStrategy
from django_pandas.io import read_frame

from main.alphavantage import SYMBOLS
from main.models import Ticker

logger = logging.getLogger(__name__)


def run_sim():
    # 2022 July 18
    # 0.36  0.45   2.74 ! [35/160] leader
    # 0.72  0.23   2.71   [70/165] rerun 0.5
    # 0.25  0.34   2.29   [25/85] rerun 0.6
    # 0.10  0.75   2.28   [10/75] rerun 0.3
    # 0.10  0.68   2.23   [10/70] rerun 0.1
    # 0.19  0.22   2.23   [20/40] rerun 0.2
    # 0.10  0.70   2.23   [10/70] rerun 0.4

    # excluding ADA
    # 0.35  0.44   2.36 ! [35/155] sigma 0.2
    # 0.36  0.45   2.31   [35/160] leader
    # 0.54  0.30   2.28   [55/160] sigma 1.5
    # 0.67  0.25   2.23   [65/170] sigma 0.4
    # 0.36  0.21   1.98   [35/75] sigma 0.6
    # 0.10  0.73   1.95   [35/265] sigma 0.1
    # 0.10  0.74   1.95   [10/75] sigma 2
    # 0.38  0.21   1.94   [40/80] sigma 0.8
    # 0.10  0.41   1.92   [10/40] sigma 0.3
    # 0.34  0.20   1.91   [35/70] sigma 0.7
    # 0.10  0.69   1.90   [10/70] sigma 1
    # 0.11  0.58   1.82   [10/65] sigma 0.5

    # added $100 weekly DCA
    # 0.35  0.44  1.80 ! [35/155] leader
    # 0.30  0.51  1.79   [30/155] s0.1
    # 0.39  0.21  1.45   [40/80] s1
    # 0.19  0.36  1.44   [20/70] s1.3
    # 0.21  0.20  1.44   [20/40] s2
    # 0.15  0.46  1.43   [15/70] s3
    # 0.10  0.45  1.42   [10/45] s0.3
    # 0.10  0.41  1.42   [10/40] s2.3
    # 0.10  0.44  1.42   [10/45] s3.3

    # week 2022 07 25
    # 0.35  0.44  1.92 ! [35/155] leader
    # 0.32  0.48  1.92   [30/155] sigma 0.03
    # 0.30  0.52  1.92   [30/155] sigma 0.13
    # 0.49  0.32  1.90   [50/155] sigma 0.33
    # 0.36  0.45  1.88   [35/160] sigma 0.01
    # 0.40  0.40  1.87   [40/160] sigma 0.1
    # 0.14  0.28  1.55   [15/40] sigma 0.4
    # 0.10  0.39  1.54   [10/40] sigma 0.2
    # 0.14  0.50  1.54   [15/70] sigma 0.23
    # 0.29  0.15  1.54   [30/45] sigma 0.3

    # changed to cagr/m for score
    # 0.20  0.40  33.24   [20/80] s0.3
    # 0.20  0.40  33.24   [20/80] s1
    # 0.20  0.40  33.24   [20/80] s3
    # 0.20  0.40  33.24   [20/80] s5
    # 0.35  0.44  31.12 ! [35/155] leader
    # 0.20  0.77  31.11   [20/155] s2
    # 0.36  0.42  29.76   [35/150] s0.01
    # 0.33  0.46  29.76   [35/150] s0.03
    # 0.38  0.40  29.70   [40/150] s0.1

    # 1 aug new leader
    # 0.20  0.40  33.15   [20/80] leader
    # 0.20  0.40  33.15   [20/80] s0.03
    # 0.20  0.40  33.15   [20/80] s0.04

    # 8 aug new leader
    # 0.20  0.40  33.10   [20/80] leader
    # 0.20  0.41  33.10   [20/80] s.03
    # 0.20  0.40  33.10   [20/80] s.1
    # 0.20  0.40  33.10   [20/80] s.3
    # 0.20  0.40  33.10   [20/80] s1
    # 0.20  0.40  33.10   [20/80] s3

    signal = 0.2
    base_mul = 0.4
    scores = []
    lowered_symbols = [s.lower() for s in SYMBOLS if s not in ['MATIC', 'DOGE', 'THETA', 'ADA']]
    for symbol in lowered_symbols:
        scores.append(get_fitness(signal, base_mul, symbols=[symbol]))
    logger.info(f'Mean score = {-np.array(scores).mean():,.2f}')
    show_current_vote(signal, base_mul, lowered_symbols)


def run_cma():
    sigma = 1
    cma_params = [
        0.2,  # signal
        0.4,  # base multiplier
    ]
    logger.info(f'CMA settings: sigma={sigma}')

    opts = CMAOptions()
    opts['timeout'] = 60 * 30
    opts['bounds'] = [
        [
            20 / 100,  # signal min
            4 / 10,  # base multiplier min
        ],
        [
            100 / 100,  # signal max
            40 / 10,  # base multiplier max
        ]
    ]
    symbols = deque([s.lower() for s in SYMBOLS if s not in ['MATIC', 'DOGE', 'THETA', 'ADA']])
    es = CMAEvolutionStrategy(cma_params, sigma, inopts=opts)
    while not es.stop():
        symbols.rotate()
        symbol = symbols[0]
        fitnesses = []
        solutions = es.ask()
        for sol in solutions:
            fitness = get_fitness(*sol, symbols=[symbol])
            fitnesses.append(fitness)
        es.tell(solutions, fitnesses)
        sol_signal, sol_base = list(es.result[5])
        logger.info(f'Solution = Signal: {round(sol_signal*20)*5:.0f} Base: {round(sol_base*10*sol_signal*20)*5:.0f}')
        es.disp()
    es.result_pretty()
    logger.info(f'finished after {es.result[3]} evaluations and {es.result[4]} iterations')


def get_fitness(signal, base_mul, symbols=None):
    if not symbols:
        symbols = [s.lower() for s in SYMBOLS]
    base = signal * base_mul * 10
    signal = int(round(signal * 20) * 5)
    base = int(round(base * 20) * 5)
    dca = 100
    withdraw = round(1200000 / 16.98 / 5200) * 100
    withdrawn = 0
    fee = 0.002
    perc = 0.01
    invest = 20_000
    invested = invest * 2
    cutoff = 100
    trades = 0
    cycles = []
    cycle = {
        'current': None,
        'previous': None,
        'usd_start': invested,
        'usd_end': invested,
        'ticks': 0,
    }
    coin_size = len(symbols)
    coin_usds = {s: 0 for s in symbols}
    coin_usds_print = {s: 0 for s in symbols}
    balances = {
        'usdt': invest,
    }
    vote = None

    df = read_frame(
        Ticker.objects.all(),
        index_col='tick_at', datetime_index=True)

    # add sma to sf
    for symbol in symbols:
        df[f'signal_{symbol}'] = df[symbol].rolling(signal).mean()
        df[f'base_{symbol}'] = df[symbol].rolling(base).mean()

    for day, ticker in df.iterrows():
        # skip if no averages
        if any(pd.isna(ticker[f'base_{s}']) for s in symbols):
            continue

        # trade only on mondays once a week (thus after sunday's close)
        if day.day_of_week != 6:
            continue

        # create coin balance now to prevent accrued price with just holding
        if len(balances) < 2:
            for symbol in symbols:
                balances[symbol] = (invest / coin_size) / ticker[symbol]

        # majority buy and sell signal
        signal_triggers = sum([ticker[f'signal_{s}'] > ticker[f'base_{s}'] for s in symbols])
        vote = (signal_triggers / coin_size) >= 0.50
        usdt_start = balances['usdt']

        # add DCA
        balances['usdt'] += dca
        invested += dca

        # WITHDRAW
        # if balances['usdt'] > withdraw:
        #     balances['usdt'] -= withdraw
        #     withdrawn += withdraw
        # else:
        #     logger.info('Not enough money to withdraw!')

        # now trade for every symbol
        for symbol in symbols:

            # sell when green
            if vote:
                portion_coin = balances[symbol] * (perc / coin_size)
                portion_usd = portion_coin * ticker[symbol]
                if portion_usd < cutoff:  # bump portion to cutoff if less
                    portion_usd = cutoff
                    portion_coin = cutoff / ticker[symbol]
                if balances[symbol] < portion_coin:
                    logger.debug(f'Not enough {portion_coin:.4f} to sell {symbol} [{balances[symbol]:.4f}]')
                else:
                    balances[symbol] -= portion_coin
                    balances['usdt'] += portion_usd * (1 - fee)
                    trades += 1
                    logger.debug(f'Selling {symbol} of {portion_usd}')

            # buy when red
            else:
                portion_usd = balances['usdt'] * (perc / coin_size)
                if portion_usd < cutoff:
                    portion_usd = cutoff
                if balances['usdt'] < portion_usd:
                    logger.debug(f'Not enough {portion_usd:.1f} to buy {symbol} [{balances["usdt"]:.0f}]')
                else:
                    balances['usdt'] -= portion_usd * (1 + fee)
                    balances[symbol] += portion_usd / ticker[symbol]
                    trades += 1
                    logger.debug(f'Buying {symbol} of {portion_usd}')

        coin_usds = {s: balances[s] * ticker[s] for s in symbols}
        coin_usds_print = {k: round(v) for k, v in coin_usds.items()}
        total_usd = balances['usdt'] + sum(coin_usds.values())
        trade = usdt_start - balances['usdt']
        logger.debug(f'{day}  trade={trade:,.0f}  TOTAL={total_usd:,.0f}  usdt={balances["usdt"]:,.0f}  coins={coin_usds_print}')

        # cycle (True is selling/bull and False is buying/bear)
        # end of cycle is when cycle goes to selling from buying crossover
        cycle['previous'], cycle['current'] = cycle['current'], vote
        cycle['ticks'] += 1
        if cycle['previous'] is False and cycle['current'] is True:
            cycle['usd_end'] = total_usd
            cycle['profit'] = cycle['usd_end'] - cycle['usd_start']
            cycle['cagr'] = cycle['profit'] ** (1 / cycle['ticks']) - 1
            logger.debug(f'End of cycle: cagr/w = {cycle["cagr"]:,.2f} (debug={cycle})')
            cycles.append(deepcopy(cycle))
            cycle['usd_start'] = total_usd
            cycle['ticks'] = 0

    ticks = len(df) * len(symbols) // 7
    part = trades / ticks
    total_return = sum(coin_usds.values()) + balances['usdt']
    cagr = (total_return - invested) ** (1 / (ticks / 4)) - 1
    if isinstance(cagr, complex):
        cagr = cagr.real
    score = (cagr * 100) * part
    vote_sym = 'S' if vote else 'B'
    logger.info(f'[{signal}/{base}-{vote_sym}] Score {score:.2f} from CAGR/m {cagr:,.2f} with part {part:.2f} for return of {total_return:,.0f} usdt={balances["usdt"]:,.0f} {coin_usds_print}')
    # logger.debug(cycles)
    return -score


def show_current_vote(signal, base_mul, symbols):
    base = signal * base_mul * 10
    signal = int(round(signal * 20) * 5)
    base = int(round(base * 20) * 5)
    coin_size = len(symbols)

    df = read_frame(
        Ticker.objects.all(),
        index_col='tick_at', datetime_index=True)

    # add sma to sf
    for symbol in symbols:
        df[f'signal_{symbol}'] = df[symbol].rolling(signal).mean()
        df[f'base_{symbol}'] = df[symbol].rolling(base).mean()
    last_row = df.iloc[-1]
    last_date = df.index[-1].date()

    # majority buy and sell signal
    signal_triggers = sum(
        [last_row[f'signal_{s}'] > last_row[f'base_{s}'] for s in symbols])
    vote = (signal_triggers / coin_size) >= 0.50
    act = 'Sell (in bull)' if vote else 'Buy (in bear)'

    logger.info(f'{last_date} voted {act}')
