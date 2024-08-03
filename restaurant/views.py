from django.shortcuts import render, get_object_or_404
from .models import MenuItem

def home(request):
    return render(request, 'restaurant/home.html')

def menu_list(request):
    items = MenuItem.objects.all()
    return render(request, 'restaurant/menu_list.html', {'items': items})

def menu_detail(request, id):
    item = get_object_or_404(MenuItem, id=id)
    return render(request, 'restaurant/menu_detail.html', {'item': item})