# Generated by Django 4.2.7 on 2023-11-30 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_mng', '0004_alter_order_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Conformed', 'Conformed'), ('Shipped', 'Shipped'), ('Delivered', 'Delevered'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_name', models.CharField(max_length=40)),
                ('streat_name', models.CharField(max_length=50)),
                ('post_office', models.CharField(max_length=20)),
                ('place', models.CharField(max_length=25)),
                ('district', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=30)),
                ('country', models.CharField(blank=True, max_length=35, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_mng.order')),
            ],
        ),
    ]
