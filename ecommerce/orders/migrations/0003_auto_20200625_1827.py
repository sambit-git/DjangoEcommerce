# Generated by Django 3.0.6 on 2020-06-25 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200625_1825'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_id',
            new_name='orderid',
        ),
    ]
