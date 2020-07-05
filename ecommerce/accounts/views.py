# django modules
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.http import is_safe_url

# user created modules inside and for this application
from .models import GuestProfile
from .forms import RegistrationForm, LoginForm, GuestRegistrationForm

def guest_register_view(request):
    form = GuestRegistrationForm(request.POST or None)
    context = {
        'form': form,
        'title': 'Guest Register',
    }
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    next_url = next_get or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        GuestProfile.objects.create(email = email)
        request.session['guest_email'] = email
        if is_safe_url(next_url, request.get_host()):
            return redirect(next_url)
    return redirect("home")

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form,
        'title': 'Login',
    }
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    next_url = next_get or next_post or None
    # print("Authenticated : ", request.user.is_authenticated)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            if is_safe_url(next_url, request.get_host()):
                return redirect(next_url)
            return redirect("home")
    return render(request, 'auth/login_page.html', context)


def registeration_page(request):
    form = RegistrationForm(request.POST or None)
    context = {
        'form': form,
        'title': 'Register',
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        User.objects.create_user(username, email, password)
        return redirect("account:login")
    return render(request, 'auth/registration_page.html', context)

def logout_page(request):
    logout(request)
    return redirect("home")