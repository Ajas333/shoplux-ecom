# Generated by Django 4.2.7 on 2023-12-10 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_log', '0015_alter_wallet_balance_alter_wallethistory_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallethistory',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]