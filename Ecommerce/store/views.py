from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.decorators.cache import cache_control

from .forms import LoginForm, RegisterForm, ProfileForm
from .models import Item, CartBase, CartItem, Profile, Order, OrderItem, PromoCode


def index(request):
    user_cart = None
    if request.user.is_authenticated:
        user_cart, created = CartBase.objects.get_or_create(user=request.user)
    context = {"products": Item.objects.all(), "user_cart": user_cart}
    return render(request, "store/index.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {"form": form}
            return render(request, "store/register.html", context)
    return render(request, "store/register.html", {"form": RegisterForm()})


def add_cart(request, id):
    if request.method == "POST":  # Ajax
        item = get_object_or_404(Item, pk=id)

        if request.user.is_authenticated:
            user = request.user
            cart, created = CartBase.objects.get_or_create(user=user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, item=item)

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()

            return JsonResponse({"cart_quantity": cart.items.count()})
        else:
            return redirect("login")
    else:
        item = get_object_or_404(Item, pk=id)

        if request.user.is_authenticated:
            user = request.user
            cart, created = CartBase.objects.get_or_create(user=user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, item=item)

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()

            return redirect("cart")
        else:
            return redirect("login")


def remove_cart(request, id):
    cart_item = get_object_or_404(CartItem, pk=id)

    if request.user.is_authenticated and cart_item.cart.user == request.user:
        cart_item.delete()

    return redirect("cart")


def view_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart, created = CartBase.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []

    return render(request, "store/cart.html", {"cart_items": cart_items, "user_cart": cart, })


def detail(request, id):
    item = Item.objects.get(pk=id)
    related_items = Item.objects.filter(category=item.category).exclude(pk=id)[:4]
    return render(request, "store/detail.html", {"item": item, "products": related_items})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(
                    request,
                    "store/login.html",
                    {"message": "Invalid Credentials", "form": LoginForm()},
                )

    elif request.method == "GET":
        return render(request, "store/login.html", {"form": LoginForm()})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def order(request):
    user = request.user
    context = {"orders": Order.objects.filter(status="Finished", user=user), }
    return render(request, "store/order.html", context)


def update_cart(request, item_id):
    user = request.user
    cart = CartBase.objects.get(user=user)
    if request.method == "POST":
        item = get_object_or_404(CartItem, id=item_id)
        nova_quantidade = int(request.POST.get("quantity"))
        if nova_quantidade <= 0:
            item.delete()
            has_item = cart.cartitem_set.exists()
            return JsonResponse({"message": "Item removido do carrinho", "itemdeleted": item_id,
                                 "has_item": has_item, "cart_quantity": cart.items.count(), })
        item.quantity = nova_quantidade
        item.save()
        item_total_price = item.total_price()
        return JsonResponse(
            {
                "message": "Quantidade atualizada com sucesso",
                "item_total_price": item_total_price,
                "cart_quantity": cart.items.count()
            }
        )


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ordered(request):
    return render(request, "store/ordered.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout(request):
    user = request.user
    if request.user.is_authenticated:
        user_cart, created = CartBase.objects.get_or_create(user=request.user)

    if request.method == "POST":
        orders = Order.objects.filter(user=user)

        if orders.exists():
            order = orders.latest('order_date')
            profile_form = ProfileForm(
                request.POST,
                instance=user.profile if hasattr(user, "profile") else None,
            )

            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                order.status = "Finished"
                order.user_profile = profile
                order.save()

                for cart_item in order.cart.cartitem_set.all():
                    OrderItem.objects.create(order=order, item=cart_item.item, quantity=cart_item.quantity)

                order.cart.delete()
                return redirect("ordered")
            else:
                return render(request, "store/checkout.html", {
                    "profile_form": profile_form,
                    "order": order,
                    "cart_items": order.cart.cartitem_set.all(),
                    "total_amount": order.calculate_total_amount(),
                    "user_cart": user_cart,
                })

    orders = Order.objects.filter(user=user)

    if orders.exists():
        order = orders.latest('order_date')
    else:
        order = Order.objects.create(user=user)
        order.cart = CartBase.objects.get(user=user)
        order.save()

    if order.status == "Finished":
        new_order = Order.objects.create(user=user)
        new_order.save()
        new_order.cart = CartBase.objects.get(user=user)
        new_order.save()
        order = new_order

    cart_items = order.cart.cartitem_set.all()
    total_amount = order.calculate_total_amount()

    try:
        profile = Profile.objects.get(user=user)
        profile_form = ProfileForm(instance=profile)
    except Profile.DoesNotExist:
        profile_form = ProfileForm()

    context = {
        "profile_form": profile_form,
        "order": order,
        "cart_items": cart_items,
        "total_amount": total_amount,
    }

    return render(request, "store/checkout.html", context)

def apply_promo_code(request):
    if request.method == "POST":
        user = request.user
        order = Order.objects.get(user=user, status="Pending")
        promo_code = request.POST.get("promo_code")

        try:
            promo = PromoCode.objects.get(code=promo_code)

            if promo.can_be_used_by_user(user):
                order.apply_promo_code(promo)
                promo.mark_as_used_by_user(user)
                return JsonResponse(
                    {
                        "message": "Código promocional aplicado com sucesso.",
                        "discount": promo.discount,
                        "updated_price": order.total_amount,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "message": "Cupom inválido ou expirado",
                        "discount": 0,
                        "updated_price": order.total_amount,
                    }
                )

        except PromoCode.DoesNotExist:
            return JsonResponse({"message": "Código promocional inválido."}, status=400)

def update_shipping_cost(request):
    if request.method == "POST":
        user = request.user
        order = Order.objects.get(user=user, status="Pending")
        shipping_option = request.POST.get("shipping_option")

        if shipping_option == "express":
            shipping_cost = Decimal(14.00)
        elif shipping_option == "post_office":
            shipping_cost = Decimal(10.00)
        elif shipping_option == "self_pickup":
            shipping_cost = Decimal(0.00)
        else:
            shipping_cost = 0.00

        order.apply_shipping(shipping_cost)

        return JsonResponse(
            {
                "message": "Custo de envio atualizado com sucesso.",
                "taxe": order.total_amount,
            }
        )
