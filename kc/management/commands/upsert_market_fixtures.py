import logging
from time import sleep

from django.core.management import BaseCommand
from kucoin.client import Market as KucoinMarket

from crarima.settings import KUCOIN_CREDS_SANDBOX
from kc.models import Market, Currency, Symbol

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'KuCoin Market Data'

    def handle(self, *args, **options):
        logger.info('Upserting market data fixtures')
        client = KucoinMarket(**KUCOIN_CREDS_SANDBOX)

        logger.info('Loading markets...')
        markets_data = client.get_market_list()
        for item in markets_data:
            market, _ = Market.objects.update_or_create(name=item)
            if _:
                logger.info(f'Added markets: {market}')

        logger.info('Loading currencies...')
        currencies_data = client.get_currencies()
        for item in currencies_data:
            currency, _ = Currency.objects.update_or_create(
                currency=item['currency'],
                defaults={
                    'name': item['name'],
                    'full_name': item['fullName'],
                    'precision': item['precision'],
                    'confirms': item['confirms'],
                    'contract_address': item['contractAddress'],
                    'withdrawal_min_size': item['withdrawalMinSize'],
                    'withdrawal_min_fee': item['withdrawalMinFee'],
                    'is_withdraw_enabled': item['isWithdrawEnabled'],
                    'is_deposit_enabled': item['isDepositEnabled'],
                    'is_margin_enabled': item['isMarginEnabled'],
                    'is_debit_enabled': item['isDebitEnabled'],
                }
            )
            if _:
                logger.info(f'Added {currency}')

        symbols_data = client.get_symbol_list()
        for item in symbols_data:
            try:
                base_currency = Currency.objects.get(currency=item['baseCurrency'])
                quote_currency = Currency.objects.get(currency=item['quoteCurrency'])
                fee_currency = Currency.objects.get(currency=item['feeCurrency'])
            except Currency.DoesNotExist:
                logger.error(f'Currency not found! {item["baseCurrency"]} or {item["quoteCurrency"]} or {item["feeCurrency"]}')
                sleep(1)
                continue
            market = Market.objects.get(name=item['market'])
            symbol, _ = Symbol.objects.update_or_create(
                symbol=item['symbol'],
                defaults={
                    'name': item['name'],
                    'base_currency': base_currency,
                    'quote_currency': quote_currency,
                    'fee_currency': fee_currency,
                    'market': market,
                    'base_min_size': item['baseMinSize'],
                    'quote_min_size': item['quoteMinSize'],
                    'base_max_size': item['baseMaxSize'],
                    'quote_max_size': item['quoteMaxSize'],
                    'base_increment': item['baseIncrement'],
                    'quote_increment': item['quoteIncrement'],
                    'price_increment': item['priceIncrement'],
                    'price_limit_rate': item['priceLimitRate'],
                    'enable_trading': item['enableTrading'],
                    'is_margin_enabled': item['isMarginEnabled'],
                    'min_funds': item.get('minFunds')
                })
            if _:
                logger.info(f'Added {symbol}')

        logger.info('done')
