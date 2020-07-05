from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView

from products.models import Product
# Create your views here.

class SearchProductListView(ListView):
    template_name = 'search/searchview.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        # print(context)
        return context

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        return Product.objects.search(query)