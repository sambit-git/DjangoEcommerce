from django.urls import path
from .views import registeration_page, login_page, logout_page, guest_register_view


app_name = 'accounts'

urlpatterns = [
    path('register/', registeration_page, name='register'),
    path('register/guest/', guest_register_view, name='guest'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
]