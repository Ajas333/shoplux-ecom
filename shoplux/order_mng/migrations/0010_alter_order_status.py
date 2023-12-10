# Generated by Django 4.2.7 on 2023-12-10 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_mng', '0009_remove_orderproduct_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Conformed', 'Conformed'), ('Shipped', 'Shipped'), ('Delivered', 'Delevered'), ('Cancelled', 'Cancelled'), ('Return', 'Return')], default='New', max_length=10),
        ),
    ]
