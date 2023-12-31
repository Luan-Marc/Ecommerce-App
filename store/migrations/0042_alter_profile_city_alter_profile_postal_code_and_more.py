# Generated by Django 4.2.5 on 2023-12-04 11:27

from django.db import migrations, models
import localflavor.br.models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0041_remove_profile_card_cvv2_remove_profile_card_expiry2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="city",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="postal_code",
            field=localflavor.br.models.BRPostalCodeField(
                max_length=9, null=True, verbose_name="CEP"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="state",
            field=localflavor.br.models.BRStateField(
                max_length=2, null=True, verbose_name="Estado"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="street",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
