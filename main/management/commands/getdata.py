import logging

from django.core.management import BaseCommand

from main.alphavantage import get_data

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Get data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delta',
            action='store_true',
            default=True,
            help='Include delta in data retrieval',
        )

    def handle(self, *args, **options):
        logger.info('Getting data...')
        delta = options['delta']
        get_data(delta)
        logger.info('done')
