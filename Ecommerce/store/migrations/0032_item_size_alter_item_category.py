# Generated by Django 4.2.5 on 2023-11-27 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0031_remove_order_cart_copy"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="size",
            field=models.CharField(
                blank=True,
                choices=[
                    ("small", "Small"),
                    ("medium", "Medium"),
                    ("large", "Large"),
                    ("extra_large", "Extra Large"),
                ],
                max_length=15,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.CharField(
                choices=[
                    ("bracelets", "Bracelets"),
                    ("dresses", "Dresses"),
                    ("earrings", "Earrrings"),
                    ("necklaces", "Necklaces"),
                    ("tshirts", "Tshirts"),
                    ("watches", "Watches"),
                    ("pants", "Pants"),
                    ("skirts", "Skirts"),
                    ("bags", "Bags"),
                ],
                max_length=20,
            ),
        ),
    ]
