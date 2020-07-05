from django.views.generic import ListView, DetailView
from .models import Product
from django.http import Http404

from carts.models import Cart
# Create your views here.


class ProductListView(ListView):
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data( *args, **kwargs)
        cart, created = Cart.objects.get_or_new(self.request)
        context['cart'] = cart
        context['title'] = 'Products'
        return context


class ProductDetailView(DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        instance = self.get_object(*args, **kwargs)
        context['title'] = f"Product: {instance.title}"
        return context
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product Doesn't Exist")
        return instance

class ProductFeaturedListView(ListView):
    queryset = Product.objects.featured()


class ProductFeaturedDetailView(DetailView):
    template_name = 'products/product_detail.html'
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Product.objects.featured().get_by_id(pk)
        if instance is None:
            raise Http404("Product Doesn't Exist")
        return instance

class ProductSlugDetailView(DetailView):
    template_name = 'products/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductSlugDetailView, self).get_context_data(*args, **kwargs)
        instance = self.get_object(*args, **kwargs)
        context['title'] = f"Product: {instance.title}"
        return context
    
    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = Product.objects.get_by_slug(slug)
        if instance is None:
            raise Http404("Product Doesn't Exist")
        return instance