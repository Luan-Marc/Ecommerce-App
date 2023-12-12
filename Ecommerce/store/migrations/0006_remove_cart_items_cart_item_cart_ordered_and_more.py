# Generated by Django 4.2.5 on 2023-10-28 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_cartitem_remove_cart_item_cart_user_delete_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.AddField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.item'),
        ),
        migrations.AddField(
            model_name='cart',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
