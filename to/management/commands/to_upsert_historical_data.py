import logging

from django.core.management import BaseCommand

from to.client import convert_trade_history
from to.models import Market

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'TradeOgre Historical Data'

    def handle(self, *args, **options):
        logger.info('Upserting historical data fixtures')
        market = Market.get_btc_usdt()
        convert_trade_history(market)
        logger.info('done')
