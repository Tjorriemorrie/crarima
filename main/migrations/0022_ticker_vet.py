# Generated by Django 4.0.4 on 2022-06-26 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_remove_ticker_bch_ticker_etc'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='vet',
            field=models.FloatField(null=True),
        ),
    ]