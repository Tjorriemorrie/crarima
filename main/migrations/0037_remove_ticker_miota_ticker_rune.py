# Generated by Django 4.0.4 on 2022-07-11 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_remove_ticker_btt_ticker_miota'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticker',
            name='miota',
        ),
        migrations.AddField(
            model_name='ticker',
            name='rune',
            field=models.FloatField(null=True),
        ),
    ]
