# Generated by Django 4.2.5 on 2023-12-04 10:04

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0033_order_promo_code_order_shipping_cost"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="card_expiration",
            field=models.DateField(
                null=True,
            ),
        ),
    ]
