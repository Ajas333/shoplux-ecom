# Generated by Django 4.2.7 on 2023-11-24 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_product_mng', '0005_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
