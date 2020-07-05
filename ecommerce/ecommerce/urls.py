"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from accounts import urls
from carts import urls
from products import urls
from search import urls
from .views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', home_page, name='home'),
    
    # Account App
    path('account/', include('accounts.urls', namespace='account')),
    # Cart App
    path('cart/', include('carts.urls', namespace = 'cart')),
    # Product App
    path('products/', include('products.urls', namespace = 'products')),
    # search App
    path('search/', include('search.urls', namespace = 'search')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
