# Generated by Django 4.2.7 on 2023-11-24 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_product_mng', '0004_cartitem_user_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
