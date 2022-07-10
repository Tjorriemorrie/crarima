import logging

import cma
from django.core.management import BaseCommand

from main.cma import run_cma, run_sim

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run CMA Evolution strategy'

    def handle(self, *args, **options):
        logger.info('Running CMA')
        # help(cma)  # "this" help message, use cma? in ipython
        # help(cma.fmin)
        # help(cma.CMAEvolutionStrategy)
        # help(cma.CMAOptions)
        # print(cma.CMAOptions('tol'))  # display 'tolerance' termination options
        # cma.CMAOptions('verb')  # display verbosity options
        # run_cma()
        run_sim()
        logger.info('done')
