from django.urls import path
from .views import ProductListView, ProductDetailView, ProductFeaturedDetailView, ProductFeaturedListView, ProductSlugDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('featured/', ProductFeaturedListView.as_view(), name='featured_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail_id'),
    path('<str:slug>/', ProductSlugDetailView.as_view(), name='detail'),
    path('featured/<int:pk>/', ProductFeaturedDetailView.as_view(), name='featured_detail')
]
