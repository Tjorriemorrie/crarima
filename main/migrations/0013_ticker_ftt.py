# Generated by Django 4.0.4 on 2022-06-24 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_ticker_uni_ticker_ltc'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='ftt',
            field=models.FloatField(null=True),
        ),
    ]
