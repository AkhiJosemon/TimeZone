# Generated by Django 4.2.4 on 2023-12-01 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_alter_coupon_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expiry_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 11, 30, 11, 15, 59, 974825, tzinfo=datetime.timezone.utc)),
        ),
    ]
