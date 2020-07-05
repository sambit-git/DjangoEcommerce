from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Cart
from orders.models import Order
from billing.models import BillingProfile
from accounts.forms import LoginForm, GuestRegistrationForm

from products.models import Product

# Create your views here.
def cart_home(request):
    cart, created = Cart.objects.get_or_new(request)
    context = {
        'cart' : cart,
        'title': 'Cart',
    }
    if created:
        print("Created new Cart: ", cart)
    else:
        print("Existing Cart: ", cart)
    return render(request, 'carts/home.html', context)

def cart_update(request):
    if request.method == "POST":
        print(request.POST)
        product_id = request.POST.get("product_id")        
        product = Product.objects.get(id=product_id)
        cart,created = Cart.objects.get_or_new(request)
        request.session["cart_count"] = cart.products.count()
        print(f"{product_id} : {product}")
        if request.POST.get("action") == "add":
            cart.products.add(product)
        elif request.POST.get("action") == "remove":
            cart.products.remove(product)
        else:
            print("code for Error")
    # return redirect("products:list")
    return redirect(request.META.get("HTTP_REFERER", "products:list"))


def checkout(request):
    cart, new = Cart.objects.get_or_new(request)
    if new or cart.products.count() == 0:
        return redirect('cart:home')
    else:
        order, created = Order.objects.get_or_create(cart = cart)
        user = request.user
        guest_email = request.session.get("guest_email")
        if user.is_authenticated:
            if guest_email:
                BillingProfile.objects.get(email = guest_email).delete()
                request.session.delete("guest_email")
                billing_profile = BillingProfile.objects.get_or_create(user = user, email = guest_email )
                del request.session["guest_email"]
            else:
                billing_profile = BillingProfile.objects.get_or_create(user = user, email = guest_email )
        else:
            if guest_email:
                billing_profile = BillingProfile.objects.get_or_create(email = guest_email)
            else:
                billing_profile = None
        guest_register_form = GuestRegistrationForm(request.POST or None)
        login_form = LoginForm(request.POST or None)
    
    context = {
        'guest_register_form' : guest_register_form,
        'login_form' : login_form,
        'billing' : billing_profile,
        'order' : order,
        'title' : 'Checkout',
    }
    return render(request, 'carts/checkout.html', context)