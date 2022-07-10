import logging
from random import random, shuffle

import pandas as pd
from cma import CMAOptions, CMAEvolutionStrategy
from django_pandas.io import read_frame

from main.alphavantage import SYMBOLS
from main.models import Ticker

logger = logging.getLogger(__name__)


def run_sim():
    # 0.64  2.64  0.002   211%   signal must be smaller than base
    # 0.35  0.47  0.499   211%   random invest amount
    # 0.10  1.02  0.001   219%   invest now 5-15 and cutoff is 1%
    # 0.33  3.89  0.001   123%   changed moving to exponential REVERTED
    # 0.20  0.43  0.001   498%   added BNB
    # 0.98  3.99  0.001   527%   cutoff back to 100
    # 0.97  3.77  0.002   480%   rounding signal and base to 10s
    # 0.31  3.85  0.002   247%   take minimum crypto return for ROI
    # 0.39  3.80  0.001   225%   invest now between 10-20k
    # 0.49  0.80  0.001   225%   added ADA
    # 0.93  3.99  0.025    88%   added SOL
    # 0.11  1.68  0.001  1428%   changed to avg returns of all instead of worst
    # 0.99  3.99  0.016   593%   changed min perc to 0001
    # 0.21  3.80  0.0432  322%   changed sigma back to 10  REVERTED
    # 1.00  4.00  0.0161  593%   bumping min amount to cutoff for trade (now balances will deplete)
    # 1.00  3.99  0.0159  594%   invest fixed to 20_000
    # 2.21  6.90  0.1000  593%   upped avg limits
    # 1.67  6.92  0.100  1352%   upped min perc to 0.001
    # 4.7  6.9  0.200   1498%   upped max perc to 20%
    # 2.5  6.9  0.200   1498%   perc rounding to 2 digits (using whole percentages [min then 0.01])
    # 2.3  9.9  0.200   1.74   378%   added participation
    # 3.1  5.5  0.07   0.69   1066%   changed participation to number of trades made (removes long N/A base values and empty wallets)
    # 2.0  6.8  0.12   0.62   1356%   max params set to max data available
    # 0.3  0.9  0.01   0.67   516%   fixed opening coin balance
    # 1.1  1.7  0.01   1.18   994%   added doge
    # 1.0  7.2  0.003   -0.01   -26%   perc now 0.0001 to 0.10  REVERTED
    # 0.2  0.7  0.01   0.90   679%   timeout set to 1 hour
    # 0.3  0.8  0.01   0.87   661%   added tron
    # 1.5  1.7  0.01   1.10   928%   sigma 6
    # 0.4  1.8  0.01   0.85   772%   sigma 7
    # 0.1  0.8  0.01   0.87   657%   sigma 5
    # 0.3  0.8  0.01   0.87   661%   sigma 8
    # 0.1  0.4  0.02   0.18   137%   dropped SOL & gain over DCA
    # 2.5  3.6  0.07   0.03   41%   DCA start balance is *2
    # 0.10  0.41  0.02   0.51   377%   removed rounding
    # 0.36  0.40  0.02   0.53   390%   base min lowered to 20
    # 0.10  0.40  0.02   0.52   383%   rerun
    # 0.93  1.69  0.01   1.36   1146%   added matic
    # 0.64  1.71  0.01   1.27   1067%   rerun
    # 0.30  1.66  0.012   1.26   1062%   halved min perc - now 0.005 from 0.01
    # 0.93  1.67  0.013   1.39   1166%   rerun
    # 1.00  1.67  0.014   1.40   1173%   rerun
    # 0.92  1.67  0.013   1.22   1027%   added ltc
    # 0.98  3.96  0.059   0.12   137%   coins are now a daily pool
    # 0.62  0.92  0.100   1.06   816%   dca proportioned to coinsize
    # 0.35  0.77  0.100    rerun
    # 0.38  0.87  0.100   1.06   817%   rerun
    # 0.34  1.70  0.05   0.87   736%   perc 0.01 to 0.20 (2 decimals and doubled max)
    # 0.19  1.65  0.05   0.87   735%   rerun
    # 0.56  0.90  0.15   0.75   578%   replaced DOGE with LINK
    # 0.45  0.92  0.15   5.28   581%   participation total needs to be weekly, not daily
    # 0.46  0.92  0.15   5.93   651%   dropped DCA subtraction
    # 0.33  0.55  0.15   6.18   654%   increased perc to 0.20
    # 0.52  0.79  0.20   5.93   647%   rerun
    # 0.34  0.77  0.17   6.03   653%   rerun
    # 0.20  0.22  0.19   6.54   667%   rerun
    # 0.30  0.90  0.10   5.86   644%   max perc of 20% WAY too volatile, bit slower.
    # 0.30  1.65   4.73   567%   hardcoded perc to 1%
    # 0.30  0.90   3.74   411%   added xlm
    # 0.30  1.65   3.96   476%   added algo
    # 0.20  1.65   3.96   475%   rerun
    # 0.25  1.65   3.94   473%   rerun
    # 0.40  0.90   5.37   586%   random 10 symbols with DOGE added back in
    # 0.30  1.75   5.43   657%   added atom (13 total)
    # 0.25  0.70   4.79   515%   added etc (14 total)
    # 0.15  1.65   5.40   643%   rerun
    # 0.50  1.70   5.16   620%   added VET (15 total)
    # 0.40  1.80   5.10   618%   rerun
    # 0.20  0.70   4.39   471%   added hbar (16 total)
    # 0.15  1.70   4.84   581%   rerun bumped sigma to 4
    # 0.80  1.75   4.99   604%   added theta (17 total)
    # 0.60  1.70   5.17   621%   rerun bumped sigma to 5
    # 0.15  1.70   5.13   615%   rerun
    # 0.20  1.70   4.71   565%   added EOS (18 total)
    # 0.85  1.60   4.76   567%   rerun (same sigma 5)
    # 0.50  0.85   4.28   467%   rerun (sigma=4 due to high variance above)
    # 0.11  0.42   4.44   466%   10/45 base is now multiplier
    # 0.13  0.58   4.13   447%   15/75 rerun sigma=0.5
    # 0.26  0.32   4.31   470%   25/80 rerun sigma=0.25
    # 0.25  0.21   4.45   468%   25/50 rerun sigma=0.2
    # 0.15  0.45   3.56   383%   15/70 added zec
    # 0.14  0.30   3.83   399%   15/40 rerun sigma 0.3
    # 0.10  0.67   3.60   384%   10/65 rerun sigma 0.15
    # 0.19  0.20   3.83   400% ! 20/40 rerun sigma 0.1
    # 0.11  0.36   3.79   396%   10/40 rerun 0.1
    # 0.13  0.64   3.57   389%   15/85 rerun 0.2

    signal = 0.13
    base_mul = 0.64
    get_fitness(signal, base_mul)


def run_cma():
    sigma = 0.2
    cma_params = [
        0.20,  # signal
        0.40,  # base multiplier
    ]
    logger.info(f'CMA settings: sigma={sigma}')

    opts = CMAOptions()
    opts['timeout'] = 60 * 30
    opts['bounds'] = [
        [
            10 / 100,  # signal min
            2 / 10,  # base multiplier min
            # 20 / 100,  # base min
            # 0.01  # perc min
        ],
        [
            100 / 100,  # signal max
            10 / 10,  # base multiplier max
            # 400 / 100,  # base max
            # 0.10  # perc max
        ]
    ]
    es = CMAEvolutionStrategy(cma_params, sigma, inopts=opts)
    while not es.stop():
        solutions = es.ask()
        fitnesses = []
        for sol in solutions:
            symbols = [s.lower() for s in SYMBOLS]
            shuffle(symbols)
            cut_symbols = symbols[:10]
            fitness = get_fitness(*sol, symbols=sorted(cut_symbols))
            fitnesses.append(fitness)
        es.tell(solutions, fitnesses)
        # sol_signal, sol_base, sol_perc = list(es.result[5])
        # logger.info(f'Solution = Signal: {round(sol_signal*20)*5:.0f} Base: {round(sol_base*20)*5:.0f} Perc: {round(sol_perc, 2)*100:.0f}%')
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
    perc = 0.01
    invest = 20_000  # randint(10_000, 20_000)
    cutoff = 100
    trades = 0
    coin_size = len(symbols)
    coin_usds = {s: 0 for s in symbols}
    coin_usds_print = {s: 0 for s in symbols}
    balances = {
        'usdt': invest,
    }

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

        # majority signal
        greens = sum([ticker[f'signal_{s}'] > ticker[f'base_{s}'] for s in symbols])
        upwards = (greens / coin_size) >= 0.50
        usdt_start = balances['usdt']

        # now trade for every symbol
        for symbol in symbols:

            # sell when green
            if upwards:
                portion_coin = balances[symbol] * (perc / coin_size)
                portion_usd = portion_coin * ticker[symbol]
                # if portion_usd < cutoff:  # bump portion to cutoff if less
                #     portion_usd = cutoff
                #     portion_coin = cutoff / ticker[symbol]
                if balances[symbol] < portion_coin:
                    logger.debug(f'Not enough {portion_coin:.4f} to sell {symbol} [{balances[symbol]:.4f}]')
                    continue
                else:
                    balances[symbol] -= portion_coin
                    balances['usdt'] += portion_usd
                    trades += 1
                    logger.debug(f'Selling {symbol} of {portion_usd}')
            # buy when red
            else:
                portion_usd = balances['usdt'] * (perc / coin_size)
                # if portion_usd < cutoff:
                #     portion_usd = cutoff
                if balances['usdt'] < portion_usd:
                    logger.debug(f'Not enough {portion_usd:.1f} to buy {symbol} [{balances["usdt"]:.0f}]')
                    continue
                else:
                    balances['usdt'] -= portion_usd
                    balances[symbol] += portion_usd / ticker[symbol]
                    trades += 1
                    logger.debug(f'Buying {symbol} of {portion_usd}')

        coin_usds = {s: balances[s] * ticker[s] for s in symbols}
        coin_usds_print = {k: round(v) for k, v in coin_usds.items()}
        total_usd = balances['usdt'] + sum(coin_usds.values())
        trade = usdt_start - balances['usdt']
        logger.debug(f'{day}  trade={trade:.0f}  TOTAL={total_usd:.0f}  RETURNS={coin_usds_print}')

    total_return = sum(coin_usds.values()) + balances['usdt']
    invested = invest * 2
    roi = (total_return - invested) / invested
    part = trades / (len(df) * len(SYMBOLS) / 7)
    score = roi * part
    logger.info(f'[{signal}/{base}] Score {score:.2f} from ROI {roi:.2f} with part {part:.2f} for return of {total_return:.0f} data={balances["usdt"]:.0f} {coin_usds_print}')
    return -score
