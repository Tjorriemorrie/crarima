# Generated by Django 4.0.4 on 2022-07-08 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='confirms',
            field=models.IntegerField(null=True),
        ),
    ]