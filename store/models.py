import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from localflavor.br.models import BRPostalCodeField, BRStateField

# Create your models here.


class Item(models.Model):

    CATEGORY_CHOICES = (
        ('bracelets', 'Bracelets'),
        ('dresses', 'Dresses'),
        ('earrings', 'Earrrings'),
        ('necklaces', 'Necklaces'),
        ('tshirts', 'Tshirts'),
        ('watches', 'Watches'),
        ('pants', 'Pants'),
        ('skirts', 'Skirts'),
        ('bags', 'Bags')
    )

    SIZE_CHOICES = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('extra_large', 'Extra Large'),
    )

    name = models.CharField(max_length=15)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    size = models.CharField(max_length=15, choices=SIZE_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CartBase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(Item, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):  # intermedio entre Cart e Item
    cart = models.ForeignKey(CartBase, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def total_price(self):
        return self.quantity * self.item.price

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=100, null=True)  # Permitindo valor nulo
    last_name = models.CharField(
        max_length=100, null=True)  # Permitindo valor nulo
    number = PhoneNumberField(null=True)

    # Email
    email = models.CharField(max_length=100, null=True)

    # Address
    number_house = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=255, null=True)
    state = BRStateField('Estado', null=True)
    postal_code = BRPostalCodeField('CEP', null=True)

    # Payment
    card_name = models.CharField(
        max_length=16, null=True)
    card_number = CardNumberField('Número do Cartão', null=True)
    card_expiration = CardExpiryField('Data de Validade', null=True)
    card_cvv = SecurityCodeField('CVV/CVC', null=True)

    def __str__(self):
        return f"Profile From: {self.user}"

class PromoCode(models.Model):
    # Código do cupom promocional
    code = models.CharField(max_length=20, unique=True)
    # Valor de desconto (porcentagem)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()  # Data de validade do cupom
    # Relacionamento muitos para muitos com usuários que já usaram o cupom
    users_used = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.code

    def can_be_used_by_user(self, user):
        """
        Verifica se o usuário pode usar o cupom.
        Retorna True se o cupom não expirou e ainda não foi usado pelo usuário.
        """
        return not self.users_used.filter(id=user.id).exists() and self.expiration_date >= timezone.now().date()

    def mark_as_used_by_user(self, user):
        """
        Marca o cupom como usado pelo usuário.
        """
        self.users_used.add(user)
        self.save()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Referência ao carrinho do usuário
    cart = models.ForeignKey(CartBase, on_delete=models.SET_NULL, null=True)
    user_profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    # Pode ser 'Pending', 'Shipped', 'Delivered', etc.
    status = models.CharField(max_length=20, default='Pending')
        # Adicione a relação ManyToMany para os itens do pedido
    items = models.ManyToManyField(Item, through='OrderItem')

        # Reference to PromoCode
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Shipping information
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return f"Order for {self.user.username} ({self.order_date})"

    def calculate_total_amount(self):
        self.total_amount = 0
        cart_items = self.cart.cartitem_set.all()

        for cart_item in cart_items:
            self.total_amount += cart_item.total_price()

        if self.promo_code:
            self.total_amount -= self.promo_code.discount
        self.save()

        return self.total_amount
    
   
    def calculate_total_itens(self):
        total_itens = 0
        order_items = OrderItem.objects.filter(order=self)  # Filtra os OrderItems relacionados a este pedido

        for order_item in order_items:
            total_itens += order_item.total_price_order()

        return total_itens

    def apply_promo_code(self, promo_code):
        try:
            promo = PromoCode.objects.get(code=promo_code)
            self.promo_code = promo
            # Aplique o desconto ao total_amount
            self.total_amount -= promo.discount
            self.save()
            return True

        except PromoCode.DoesNotExist:
            return False

    def apply_shipping(self, shipping_cost):
        self.shipping_cost = shipping_cost
        #self.calculate_total_amount()
        #self.total_amount += shipping_cost
        self.total_amount = self.calculate_total_amount() + shipping_cost
        self.save()
        return True

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"Order: {self.order.user.username} - From: {self.order.order_date}"

    def total_price_order(self):
        return self.quantity * self.item.price
