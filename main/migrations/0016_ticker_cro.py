# Generated by Django 4.0.4 on 2022-06-24 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_ticker_xlm'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='cro',
            field=models.FloatField(null=True),
        ),
    ]