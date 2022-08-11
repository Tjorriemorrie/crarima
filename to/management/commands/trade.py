import logging
from time import sleep

from django.core.management import BaseCommand
from kucoin.client import Trade

from crarima.settings import KUCOIN_CREDS_SANDBOX
from kc.constants import SYMBOL_BTC_USDT, TRADE_SIDE_BUY

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'KuCoin Trade'

    def handle(self, *args, **options):
        logger.info('Trading...')
        client = Trade(**KUCOIN_CREDS_SANDBOX)

        # place a limit buy order
        order_id = client.create_limit_order(SYMBOL_BTC_USDT, TRADE_SIDE_BUY, '1', '8000')['orderId']
        logger.info(f'Created limited order {order_id}')
        sleep(3)

        # place a market buy order   Use cautiously
        # order_id = client.create_market_order('BTC-USDT', 'buy', size='1')

        # cancel limit order
        res = client.cancel_order(order_id)
        logger.info(f'Cancelled limited order: {res}')

        logger.info('done')
