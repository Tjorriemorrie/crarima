import logging

import ccxt
from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django.db.models import Max
from django.utils.timezone import now, make_aware

from options.models import Currency, OHLC

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Get CCTX btc data'

    def handle(self, *args, **options):
        currency = get_currency()
        logger.info(f'Updating {currency}')

        # Get the biggest 'at' value for the given currency
        biggest_at = OHLC.objects.filter(currency=currency).aggregate(Max('at'))['at__max']
        if not biggest_at:
            biggest_at = now() - timedelta(days=365*8)
        # Convert datetime to Unix timestamp in milliseconds
        since_timestamp = int(biggest_at.timestamp() * 1000)
        logger.info(f'Querying exchange from {biggest_at}')

        # Fetch historical data
        historical_data = fetch_historical_data(
            currency.exchange, currency.symbol, currency.timeframe, since_timestamp)
        logger.info(f'Found {len(historical_data)} new prices')

        # Print the fetched data
        for data in historical_data:
            timestamp = make_aware(datetime.utcfromtimestamp(data[0] / 1000))
            ohlc, created = OHLC.objects.update_or_create(
                currency=currency,
                at=timestamp,
                defaults={
                    'open': data[1],
                    'high': data[2],
                    'low': data[3],
                    'close': data[4],
                    'volume': data[5],
                }
            )
            logger.info(f'{"Created" if created else "Updated"} {ohlc}')


def get_currency() -> Currency:
    currency, _ = Currency.objects.get_or_create(
        exchange='binance',  # Change this to your desired exchange
        symbol='BTC/USDT',  # Change this to the desired trading pair
        timeframe='1d'  # Daily timeframe
    )
    return currency


def fetch_historical_data(exchange, symbol, timeframe, since):
    # Create an instance of the exchange
    exchange_instance = getattr(ccxt, exchange)()
    limit = 1000  # Maximum number of items per request
    result = []

    while True:
        # Load historical data
        ohlcv = exchange_instance.fetch_ohlcv(symbol, timeframe, since, limit)
        if not ohlcv:
            break

        result.extend(ohlcv)

        # Update 'since' to fetch next batch
        since = ohlcv[-1][0] + 1  # Set 'since' to the timestamp of the last item + 1

    return result
