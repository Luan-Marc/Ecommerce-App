# Generated by Django 4.2.5 on 2023-10-28 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_cart_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='item',
        ),
    ]
