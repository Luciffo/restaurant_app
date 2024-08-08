from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Dish
from django.views.generic import ListView

def home(request):
    return render(request, 'restaurant/home.html')

def menu_list(request):
    items = MenuItem.objects.all()
    return render(request, 'restaurant/menu_list.html')

def menu_detail(request, id):
    item = get_object_or_404(MenuItem, id=id)
    return render(request, 'restaurant/menu_detail.html')

def menu_list(request):
    first_dish = Dish.objects.first()  # Получаем первое блюдо
    return render(request, 'restaurant/menu_list.html', {'first_dish': first_dish})

class DishListView(ListView):
    model = Dish
    context_object_name = "dishes"
    template_name = "restaurant/menu_list.html"