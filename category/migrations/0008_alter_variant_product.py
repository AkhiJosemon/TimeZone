# Generated by Django 4.2.4 on 2023-11-15 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0007_variant_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.product'),
        ),
    ]