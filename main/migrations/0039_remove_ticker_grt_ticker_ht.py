# Generated by Django 4.0.4 on 2022-07-11 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_remove_ticker_rune_ticker_grt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticker',
            name='grt',
        ),
        migrations.AddField(
            model_name='ticker',
            name='ht',
            field=models.FloatField(null=True),
        ),
    ]