# Generated by Django 4.2.7 on 2023-11-19 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_log', '0009_alter_accountuser_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user_log.address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/image_admin/people'),
        ),
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.CharField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='AccountUser',
        ),
    ]
