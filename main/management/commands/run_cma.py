import logging

from django.core.management import BaseCommand

from main.cma import run_cma, run_sim

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run CMA Evolution strategy'

    def handle(self, *args, **options):
        logger.info('Running CMA')

        run_cma()
        # run_sim()

        logger.info('done')
