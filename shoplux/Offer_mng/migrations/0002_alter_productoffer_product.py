# Generated by Django 4.2.7 on 2023-12-04 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_det', '0004_alter_product_variant_product_variant_slug'),
        ('Offer_mng', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoffer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productoffer_set', to='product_det.product'),
        ),
    ]
