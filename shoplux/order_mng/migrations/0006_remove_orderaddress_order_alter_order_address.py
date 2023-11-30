# Generated by Django 4.2.7 on 2023-11-30 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_mng', '0005_alter_order_status_orderaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderaddress',
            name='order',
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_mng.orderaddress'),
        ),
    ]
