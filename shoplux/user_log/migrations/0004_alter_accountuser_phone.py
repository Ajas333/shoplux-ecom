# Generated by Django 4.2.7 on 2023-11-18 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_log', '0003_accountuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountuser',
            name='phone',
            field=models.CharField(),
        ),
    ]
