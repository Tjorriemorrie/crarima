# Generated by Django 4.0.4 on 2022-06-21 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_ticker_eth'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='bnb',
            field=models.FloatField(null=True),
        ),
    ]