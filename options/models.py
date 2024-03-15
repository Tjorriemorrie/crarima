from django.db import models


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Currency(TimeStamped):
    symbol = models.CharField(max_length=50)
    exchange = models.CharField(max_length=50)
    timeframe = models.CharField(max_length=10)

    def __str__(self):
        return f'<Currency {self.symbol} at {self.timeframe} from {self.exchange}>'


class OHLC(TimeStamped):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='ohlcs')
    at = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()

    def __str__(self):
        return f'<OHLC {self.currency.symbol} {self.at} {self.close}>'
