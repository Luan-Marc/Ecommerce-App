from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('cart', views.view_cart, name="cart"),
    path('add/<int:id>/', views.add_cart, name='add_cart'),
    path('remove/<int:id>/', views.remove_cart, name='remove_cart'),
    path('register', views.register, name="register"),
    path('order', views.order, name="order"),
    path('check/<int:id>/', views.detail, name='detail'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('apply_promo_code/', views.apply_promo_code, name='apply_promo_code'),
    path('update_shipping_cost/', views.update_shipping_cost, name='update_shipping_cost'),
    path('ordered/', views.ordered, name='ordered')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
