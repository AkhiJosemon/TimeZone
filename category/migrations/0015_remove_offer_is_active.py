# Generated by Django 4.2.4 on 2023-12-01 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0014_offer_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='is_active',
        ),
    ]
