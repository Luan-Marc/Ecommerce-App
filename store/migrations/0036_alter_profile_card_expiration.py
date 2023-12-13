# Generated by Django 4.2.5 on 2023-12-04 10:08

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0035_alter_profile_card_expiration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="card_expiration",
            field=models.DateField(
                max_length=7,
                null=True,
            ),
        ),
    ]