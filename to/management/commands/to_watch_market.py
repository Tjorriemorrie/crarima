import logging

from django.core.management import BaseCommand

from to.client import TradeOgreClient, watch_market
from to.models import Market

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'TradeOgre Watch Market to gather data'

    def handle(self, *args, **options):
        market = Market.get_btc_usdt()
        watch_market(market)
