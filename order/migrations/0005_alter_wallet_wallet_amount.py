# Generated by Django 4.2.4 on 2023-11-27 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_amount',
            field=models.FloatField(default=0),
        ),
    ]
