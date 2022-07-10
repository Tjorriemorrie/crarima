import logging

from django.core.management import BaseCommand

from main.alphavantage import get_data

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Get data'

    def handle(self, *args, **options):
        logger.info('Getting data...')
        get_data(delta=False)
        logger.info('done')
