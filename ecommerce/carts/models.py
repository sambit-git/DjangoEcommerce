from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed, pre_save
from decimal import Decimal
# Create your models here.

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def get_or_new(self, request):
        cart_id = request.session.get("cart_id", None)
        if cart_id is None:
            cart = self.new(user = request.user)
            request.session["cart_id"] = cart.id
            request.session["cart_count"] = 0
            created = True
        else:
            cart = self.get_queryset().get(id = cart_id)
            request.session["cart_count"] = cart.products.count()
            if cart.user is None and request.user.is_authenticated:
                cart.user = request.user
                cart.save()
            created = False
        return cart,created
    
    def new(self, user = None):
        if user.is_authenticated:
            cart = self.get_queryset().create(user = user)
        else:
            cart = self.get_queryset().create(user = None)
        return cart

class Cart(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank = True)
    subtotal = models.DecimalField(max_digits=10, default=0.00, decimal_places=2)
    total = models.DecimalField(max_digits=10, default=0.00, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return f"{self.id} - {self.user}"


def m2mreceiver(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        total = 0
        for product in instance.products.all():
            total += product.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2mreceiver, sender=Cart.products.through)


def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.total = Decimal(instance.subtotal) + Decimal(0.18) * Decimal(instance.subtotal)

pre_save.connect(pre_save_receiver, sender=Cart)