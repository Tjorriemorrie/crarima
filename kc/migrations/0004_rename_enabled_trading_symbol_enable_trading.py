# Generated by Django 4.0.4 on 2022-07-08 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kc', '0003_alter_currency_is_deposit_enabled_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='symbol',
            old_name='enabled_trading',
            new_name='enable_trading',
        ),
    ]