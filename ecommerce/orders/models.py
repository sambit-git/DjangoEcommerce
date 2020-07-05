from django.db import models
from django.db.models.signals import post_save,pre_save
from carts.models import Cart
from .utils import unique_id_generator
from decimal import Decimal

order_status_choices = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)

# Create your models here.
class Order(models.Model):
    orderid = models.CharField(max_length = 120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length = 120, default = "created", choices=order_status_choices)
    shipping_total = models.DecimalField(default=5.99, max_digits=7, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.orderid

    def calculate_order_total(self):
        self.total = Decimal(self.cart.total) + Decimal(self.shipping_total)
        return self.total


def order_pre_save_receiver(sender, instance, *args, **kwargs):
    print("Instance.orderid: ", len(instance.orderid))
    if not instance.orderid:
        instance.orderid = unique_id_generator(instance)
    instance.calculate_order_total()

pre_save.connect(order_pre_save_receiver, sender=Order)


def post_save_create_order_from_cart(sender, instance, *args, **kwargs):
    order, created = Order.objects.get_or_create(cart = instance)
    order.save()

post_save.connect(post_save_create_order_from_cart, sender=Cart)