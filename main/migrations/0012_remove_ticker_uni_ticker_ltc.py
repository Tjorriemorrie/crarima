# Generated by Django 4.0.4 on 2022-06-24 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_ticker_uni'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticker',
            name='uni',
        ),
        migrations.AddField(
            model_name='ticker',
            name='ltc',
            field=models.FloatField(null=True),
        ),
    ]