# Generated by Django 4.2.4 on 2023-11-16 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
