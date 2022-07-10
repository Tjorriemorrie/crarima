import logging
from copy import copy
from time import sleep, time

from django.core.management import BaseCommand
from kucoin.client import Market as KucoinMarket

from crarima.settings import KUCOIN_CREDS_SANDBOX
from kc.constants import SYMBOL_BTC_USDT, INTERVAL_1MIN, INTERVAL_1MIN_SECONDS
from kc.models import Market, Currency, Symbol, Ticker, Timestamp

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'KuCoin Historical Data'

    def handle(self, *args, **options):
        logger.info('Upserting historical data fixtures')
        creds = copy(KUCOIN_CREDS_SANDBOX)
        creds['is_sandbox'] = False
        client = KucoinMarket(**creds)

        for symbol_name in [SYMBOL_BTC_USDT]:
            symbol = Symbol.objects.get(symbol=symbol_name)
            logger.info(f'Loading historical data for {symbol.name}...')

            # end_at = int(round(time()))
            start_at = int(round(time())) - INTERVAL_1MIN_SECONDS
            # end_at = None
            ts = {0: [], 1: []}
            has_created = True
            for i in range(2):
            # while has_created:
                data = client.get_kline(
                    symbol.symbol, INTERVAL_1MIN, startAt=start_at)
                ts[i] = [k[0] for k in data]
                a = 1
                for item in data:
                    timestamp, _ = Timestamp.objects.update_or_create(
                        seconds=int(item[0]))
                    ticker, created = Ticker.objects.update_or_create(
                        tick_at=timestamp,
                        symbol=symbol,
                        defaults={
                            'time': int(item[0]),
                            'open': float(item[1]),
                            'close': float(item[2]),
                            'high': float(item[3]),
                            'low': float(item[4]),
                            'volume': float(item[5]),
                            'turnover': float(item[6]),
                        })
                    has_created = has_created or created
                    logger.info(f'Added ticker: {ticker}')
                end_at = data[-1][0]

        logger.info('done')
