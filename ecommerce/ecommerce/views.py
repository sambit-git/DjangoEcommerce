# django modules
from django.shortcuts import render


def home_page(request):
    context = {
        'title': 'Home Page',
    }
    # print(request.get_host())
    return render(request, 'home.html', context)