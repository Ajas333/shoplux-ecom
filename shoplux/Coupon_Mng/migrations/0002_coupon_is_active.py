# Generated by Django 4.2.7 on 2023-12-04 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Coupon_Mng', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]