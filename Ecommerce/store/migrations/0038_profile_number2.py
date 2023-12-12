# Generated by Django 4.2.5 on 2023-12-04 10:57

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0037_alter_profile_card_expiration"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="number2",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, null=True, region=None
            ),
        ),
    ]
