import logging

from django.core.management import BaseCommand

from main.ml import test_model, predict_btc_100, grid_search_buy_sell, grid_search_buy_sell_ewm

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Build models'

    def handle(self, *args, **options):
        logger.info('testing model...')
        # test_model()
        # predict_btc_100()
        # grid_search_buy_sell()
        grid_search_buy_sell_ewm()
        logger.info('done')
