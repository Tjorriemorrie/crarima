# Generated by Django 4.0.4 on 2022-06-21 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_ticker_ada'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='sol',
            field=models.FloatField(null=True),
        ),
    ]
