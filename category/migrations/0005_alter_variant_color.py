# Generated by Django 4.2.4 on 2023-11-15 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_rename_stocks_product_total_stocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='color',
            field=models.CharField(blank=True, choices=[('black', 'Black'), ('silver', 'Silver'), ('brown', 'brown'), ('golden', 'Golden'), ('blue', 'Blue'), ('red', 'Red'), ('green', 'Green')], max_length=50),
        ),
    ]
