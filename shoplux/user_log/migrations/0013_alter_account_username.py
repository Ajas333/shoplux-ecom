# Generated by Django 4.2.7 on 2023-11-27 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_log', '0012_remove_account_address_address_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]