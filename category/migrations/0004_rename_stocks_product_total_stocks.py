# Generated by Django 4.2.4 on 2023-11-14 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_variant_stocks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stocks',
            new_name='total_stocks',
        ),
    ]
