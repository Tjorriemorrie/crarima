from django.contrib import admin

from main.models import Ticker


@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ['tick_at', 'price', 'btc', 'xmr']
    ordering = ['-tick_at']
