# Generated by Django 4.0.4 on 2022-07-11 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_remove_ticker_kcs_ticker_zec'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='mkr',
            field=models.FloatField(null=True),
        ),
    ]
