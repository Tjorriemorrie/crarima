from datetime import datetime

from django.db import models
from django.utils.timezone import make_aware

from to.constants import MARKET_BTC_USDT


class Market(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}'

    @staticmethod
    def get_btc_usdt() -> 'Market':
        return Market.objects.get(name=MARKET_BTC_USDT)


# class Currency(models.Model):
#     currency = models.CharField(max_length=20, unique=True)
#     name = models.CharField(max_length=50)
#     full_name = models.CharField(max_length=150)
#     precision = models.IntegerField()
#     confirms = models.IntegerField(null=True)
#     contract_address = models.CharField(max_length=250, null=True)
#     withdrawal_min_size = models.FloatField(null=True)
#     withdrawal_min_fee = models.FloatField(null=True)
#     is_withdraw_enabled = models.BooleanField(null=True)
#     is_deposit_enabled = models.BooleanField(null=True)
#     is_margin_enabled = models.BooleanField()
#     is_debit_enabled = models.BooleanField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self) -> str:
#         return f'{self.currency}(currency)'
#
#
# class Symbol(models.Model):
#     symbol = models.CharField(max_length=20, unique=True)
#     name = models.CharField(max_length=50)
#     base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='base_symbols')
#     quote_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='quote_symbols')
#     fee_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='fee_symbols')
#     market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='symbols')
#     base_min_size = models.FloatField()
#     quote_min_size = models.FloatField()
#     base_max_size = models.FloatField()
#     quote_max_size = models.FloatField()
#     base_increment = models.FloatField()
#     quote_increment = models.FloatField()
#     price_increment = models.FloatField()
#     price_limit_rate = models.FloatField()
#     enable_trading = models.BooleanField()
#     is_margin_enabled = models.BooleanField()
#     min_funds = models.FloatField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self) -> str:
#         return f'{self.symbol}(symbol)'
#
#
# class Timestamp(models.Model):
#     seconds = models.PositiveBigIntegerField(unique=True)
#     minute = models.DateTimeField(unique=True)
#
#     def __str__(self) -> str:
#         return f'{self.minute:"%Y-%m-%d %H:%M"}'
#
#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#         if not self.minute:
#             self.minute = make_aware(datetime.fromtimestamp(self.seconds))
#         return super().save(force_insert, force_update, using, update_fields)


class Ticker(models.Model):
    tick_at = models.DateTimeField(db_index=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='tickers')
    price = models.FloatField()
    is_trade = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tick_at']

    def __str__(self) -> str:
        rep = f'{self.market} {self.tick_at:%Y-%m-%d %H:%M} {self.price:,.2f}'
        if self.is_trade:
            rep += ' (was trade)'
        return rep
