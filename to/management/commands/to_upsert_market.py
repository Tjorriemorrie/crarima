import logging

from django.core.management import BaseCommand

from to.client import TradeOgreClient
from to.models import Market

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'TradeOgre Market Data'

    def handle(self, *args, **options):
        logger.info('Upserting market data fixtures')

        logger.info('Loading markets...')
        client = TradeOgreClient()
        data = client.list_markets()
        for item in data:
            for key in item.keys():
                market, created = Market.objects.update_or_create(name=key)
                logger.info(f'{created and "Created" or "Updated"} {market}')

        logger.info('done')
