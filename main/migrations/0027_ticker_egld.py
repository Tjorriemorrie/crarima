# Generated by Django 4.0.4 on 2022-06-30 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_ticker_theta'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='egld',
            field=models.FloatField(null=True),
        ),
    ]
