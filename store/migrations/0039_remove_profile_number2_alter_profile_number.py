# Generated by Django 4.2.5 on 2023-12-04 10:58

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0038_profile_number2"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="number2",
        ),
        migrations.AlterField(
            model_name="profile",
            name="number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, null=True, region=None
            ),
        ),
    ]
