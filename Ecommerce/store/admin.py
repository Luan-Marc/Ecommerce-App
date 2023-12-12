from django.contrib import admin
from django.contrib.auth.models import User
from .models import Item, CartBase, CartItem, Profile, Order, PromoCode, OrderItem
# Register your models here.

admin.site.register(Item)
admin.site.register(CartBase)
admin.site.register(CartItem)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PromoCode)
