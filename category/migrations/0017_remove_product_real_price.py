# Generated by Django 4.2.4 on 2023-12-01 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0016_product_real_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='real_price',
        ),
    ]