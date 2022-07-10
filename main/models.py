import logging

from django.db import models

logger = logging.getLogger(__name__)


class Ticker(models.Model):
    tick_at = models.DateTimeField()
    btc = models.FloatField(null=True)
    xmr = models.FloatField(null=True)
    eth = models.FloatField(null=True)
    bnb = models.FloatField(null=True)
    ada = models.FloatField(null=True)
    # sol = models.FloatField(null=True)
    doge = models.FloatField(null=True)
    # dot = models.FloatField(null=True)
    trx = models.FloatField(null=True)
    # avax = models.FloatField(null=True)
    matic = models.FloatField(null=True)
    # uni = models.FloatField(null=True)
    ltc = models.FloatField(null=True)
    # ftt = models.FloatField(null=True)
    link = models.FloatField(null=True)
    xlm = models.FloatField(null=True)
    # cro = models.FloatField(null=True)
    algo = models.FloatField(null=True)
    atom = models.FloatField(null=True)
    # bch = models.FloatField(null=True)
    etc = models.FloatField(null=True)
    vet = models.FloatField(null=True)
    # mana = models.FloatField(null=True)
    # flow = models.FloatField(null=True)
    hbar = models.FloatField(null=True)
    theta = models.FloatField(null=True)
    eos = models.FloatField(null=True)
    zec = models.FloatField(null=True)

    arima = models.FloatField(null=True)
    garch = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tick_at']

    def __str__(self):
        return f'<Tick {self.tick_at} {self.price:.4f}>'

    @property
    def price(self) -> float:
        if not self.btc or not self.xmr:
            return 0
        return self.xmr / self.btc


# class NoTxError(Exception):
#     """No quote as no tx."""
#
#
# class NoHistoryError(Exception):
#     """No history as on portfolio."""
#
#
# class NoQuoteError(Exception):
#     """No quote as on crypto_asset."""
#
#
# class SellTransactionError(Exception):
#     """Selling more than you have."""
#
#
# class Snapshot(models.Model):
#     snapped_at = models.DateField(unique=True)
#     href = models.CharField(max_length=55)
#     completed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ('snapped_at',)
#
#     def __str__(self):
#         return f'<Snapshot {self.snapped_at}>'
#
#
# class Quote(models.Model):
#     snapshot = models.ForeignKey(
#         Snapshot, on_delete=models.CASCADE, related_name='quotes')
#     cryptocurrency = models.ForeignKey(
#         CryptoCurrency, on_delete=models.CASCADE, related_name='quotes')
#     rank = models.IntegerField()
#
#     max_supply = models.IntegerField(null=True)
#     circulating_supply = models.IntegerField()
#     total_supply = models.IntegerField()
#     price = models.FloatField()
#     volume_24h = models.FloatField()
#     change_7d = models.FloatField()
#     market_cap = models.FloatField()
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = ('snapshot', 'cryptocurrency', 'rank')
#         ordering = ('snapshot', 'rank')
#
#     def __str__(self) -> str:
#         return f'<Quote {self.cryptocurrency.symbol} #{self.rank} {self.snapshot.snapped_at}>'
#
#
# class Portfolio(models.Model):
#     CHOICES_STRATEGIES = (
#         (STRATEGY_HODL, 'hodl'),
#         (STRATEGY_REBALL, 'reball'),
#         (STRATEGY_REBALL_GROWTH_1, 'reball_growth_1'),
#         (STRATEGY_REBALL_GROWTH_3, 'reball_growth_3'),
#         (STRATEGY_REBALL_GROWTH_5, 'reball_growth_5'),
#         (STRATEGY_REBALL_GROWTH_2, 'reball_growth_2'),
#         (STRATEGY_REBALL_GAINER_1, 'reball_gainer_1'),
#         (STRATEGY_REBALL_GROFAST_1, 'reball_grofast_1'),
#         (STRATEGY_REBALL_GROFAST_2, 'reball_grofast_2'),
#         (STRATEGY_REBALL_GROFAST_3, 'reball_grofast_3'),
#         (STRATEGY_REBALL_GROFAST_5, 'reball_grofast_5'),
#         (STRATEGY_REBALL_GROCAY_1, 'reball_grocay_1'),
#         (STRATEGY_REBALL_GROCAY_2, 'reball_grocay_2'),
#         (STRATEGY_REBALL_GROCAY_3, 'reball_grocay_3'),
#         (STRATEGY_REBALL_GROCAY_5, 'reball_grocay_5'),
#     )
#
#     size = models.IntegerField(default=10)
#     starting_balance = models.FloatField(default=100)
#     strategy = models.IntegerField(choices=CHOICES_STRATEGIES, default=STRATEGY_HODL)
#     last_run_at = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = ('size', 'strategy')
#
#     def __str__(self):
#         return f'<Portfolio Top {self.size} {self.strategy_name} ' \
#                f'start={self.starting_balance}>'
#
#     @property
#     def strategy_name(self):
#         strategy_opt = [s for s in self.CHOICES_STRATEGIES if s[0] == self.strategy]
#         return strategy_opt[0][1]
#
#     def current_assets(self):
#         return [ca for ca in self.assets.all() if ca.total_units]
#
#
# class CryptoAsset(models.Model):
#     portfolio = models.ForeignKey(
#         Portfolio, on_delete=models.CASCADE, related_name='assets')
#     cryptocurrency = models.ForeignKey(
#         CryptoCurrency, on_delete=models.CASCADE, related_name='assets')
#     alloc = models.FloatField()
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = ('portfolio', 'cryptocurrency')
#
#     def __str__(self) -> str:
#         return f'<Asset #{self.last_rank} {self.cryptocurrency.symbol} {round(self.alloc * 100, 1)}% ' \
#                f'value={self.total_value} units={round(self.total_units, 8)}'
#
#     @property
#     def total_units(self) -> float:
#         val = self.txs.aggregate(Sum('units'))['units__sum']
#         return val or 0
#
#     @property
#     def total_value(self) -> float:
#         try:
#             return int(self.total_units * self.last_quote.price)
#         except NoQuoteError as exc:
#             return 0
#
#     @property
#     def last_rank(self) -> int:
#         try:
#             return self.last_quote.rank
#         except NoQuoteError as exc:
#             return -1
#
#     @property
#     def last_quote(self) -> Quote:
#         history = PortfolioSnapshot.objects.filter(portfolio=self.portfolio).last()
#         if not history:
#             raise NoQuoteError()
#         quote = Quote.objects.filter(
#             cryptocurrency=self.cryptocurrency,
#             snapshot__snapped_at__lte=history.snapshot.snapped_at
#         ).order_by('-snapshot__snapped_at').first()
#         if not quote:
#             raise NoQuoteError('No quote found')
#         return quote
#
#
# class Transaction(models.Model):
#     crypto_asset = models.ForeignKey(
#         CryptoAsset, on_delete=models.CASCADE, related_name='txs')
#     quote = models.ForeignKey(
#         Quote, on_delete=models.CASCADE, related_name='txs')
#     units = models.FloatField()
#     is_initial = models.BooleanField(default=False)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     # class Meta:
#     #     unique_together = ('crypto_asset', 'quote')
#
#     def __str__(self) -> str:
#         return f'<Tx {self.crypto_asset.cryptocurrency.symbol} value={self.value} ' \
#                f'units={round(self.units, 8)}>'
#
#     @property
#     def value(self) -> float:
#         return int(self.units * self.quote.price)
#
#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None):
#         if self.units == 0:
#             raise SellTransactionError('No units in tx')
#         if self.units < 0 and abs(self.units) > self.crypto_asset.total_units:
#             raise SellTransactionError(
#                 f'Trying to sell {self.units} but only '
#                 f'have {self.crypto_asset.total_units}')
#         super().save(force_insert, force_update, using, update_fields)
#
#
# class PortfolioSnapshot(models.Model):
#     portfolio = models.ForeignKey(
#         Portfolio, on_delete=models.CASCADE, related_name='histories')
#     snapshot = models.ForeignKey(
#         Snapshot, on_delete=models.CASCADE, related_name='histories')
#
#     snapped_at = models.DateField()
#     size = models.IntegerField()
#     weight = models.FloatField()
#     invest = models.FloatField()
#     market = models.FloatField()
#     gain = models.FloatField()
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = ('portfolio', 'snapshot')
#         ordering = ('portfolio', 'snapped_at')
#
#     def __str__(self) -> str:
#         return f'<PortSnap {self.snapped_at} {self.size} {self.invest} {self.market} {self.gain * 100}%>'
