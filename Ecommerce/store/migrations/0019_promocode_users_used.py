# Generated by Django 4.2.5 on 2023-11-09 10:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0018_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='users_used',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]