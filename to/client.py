import logging
from datetime import datetime, timedelta
from time import sleep

import requests
from django.utils.timezone import make_aware, now
from retry import retry

from to.models import Market, Ticker

logger = logging.getLogger(__name__)


class TooManyRequestsError(Exception):
    """Too many http requests."""


class RequestsError(Exception):
    """SSL error from BGG."""


class TradeOgreError(Exception):
    """Trade ogre non-success."""


sleep_time = 0
last_url = None


@retry((TooManyRequestsError, RequestsError), delay=5, jitter=1, max_delay=60)
def get(url: str) -> requests.Response:
    global sleep_time
    global last_url
    # if last_url == url:
    #     sleep_time = round(sleep_time + 0.5, 3)
    #     logger.info(f'Increased sleep time to {sleep_time}')
    if sleep_time:
        sleep_time = round(sleep_time - 0.005, 3)
    last_url = url
    sleep(sleep_time)

    try:
        res = requests.get(url)
    except Exception as exc:
        logger.warning(f'Connection error! {exc}')
        raise RequestsError() from exc
    if res.status_code == 429:
        logger.warning(f'Too many requests! {url}')
        raise TooManyRequestsError()
    elif res.status_code >= 500:
        logger.warning(f'Server error! {url}')
        raise TooManyRequestsError()
    res.raise_for_status()
    return res.json()


class TradeOgreClient:
    host = 'https://tradeogre.com/api/v1'

    def list_markets(self):
        url = f'{self.host}/markets'
        data = get(url)
        return data

    def get_ticker(self, market_name: str):
        url = f'{self.host}/ticker/{market_name}'
        data = get(url)
        if not data['success']:
            raise TradeOgreError(f'No success {data} at {url}')
        return data

    def get_trade_history(self, market_name: str):
        url = f'{self.host}/history/{market_name}'
        data = get(url)
        return data


def _dt_from_ts(ts: int) -> datetime:
    dt = datetime.fromtimestamp(ts)
    dt = make_aware(dt)
    dt = dt.replace(second=0, microsecond=0)
    return dt


def convert_trade_history(market: Market):
    logger.info(f'Converting trade history to tickers for {market}')

    client = TradeOgreClient()
    data = client.get_trade_history(market.name)

    for item in data:
        dt = _dt_from_ts(item['date'])
        # manually upsert due to is_trade flag
        try:
            ticker = Ticker.objects.get(market=market, tick_at=dt)
        except Ticker.DoesNotExist:
            ticker = Ticker.objects.create(
                market=market,
                tick_at=dt,
                is_trade=True,
                price=float(item['price'])
            )
        logger.info(f'{ticker}')


def _get_dt():
    dt = now()
    dt = dt.replace(second=0, microsecond=0)
    return dt


def _wait_till_next_min():
    one_min_ahead = (now() + timedelta(seconds=60)).replace(second=0, microsecond=0)
    wait_delta = (one_min_ahead - now()).seconds
    logger.info(f'sleeping for {wait_delta}s...')
    sleep(wait_delta)


def watch_market(market: Market):
    logger.info(f'Watching {market}...')
    client = TradeOgreClient()
    while True:
        data = client.get_ticker(market.name)
        ticker, created = Ticker.objects.update_or_create(
            market=market,
            tick_at=_get_dt(),
            defaults={
                'price': float(data['price'])
            }
        )
        logger.info(f'{created and "Created" or "Updated"} {ticker}')
        _wait_till_next_min()
