# Generated by Django 4.2.6 on 2023-12-10 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0023_product_temp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]