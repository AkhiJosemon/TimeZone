# Generated by Django 4.2.4 on 2023-11-30 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_alter_coupon_expiry_date_redeemed_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='redeemed_coupon',
            name='is_redeemed',
        ),
        migrations.AlterField(
            model_name='coupon',
            name='expiry_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 11, 29, 9, 0, 33, 174147, tzinfo=datetime.timezone.utc)),
        ),
    ]
