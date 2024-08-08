from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, CartItem, Cart, MenuItem
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def home(request):

    return render(request, 'restaurant/home.html')

def menu_list(request):
    items = MenuItem.objects.all()
    return render(request, 'restaurant/menu_list.html')

def menu_detail(request, id):
    item = get_object_or_404(MenuItem, id=id)
    return render(request, 'restaurant/menu_detail.html')

class DishListView(ListView):
    model = Dish
    context_object_name = "dishes"
    template_name = "restaurant/menu_list.html"

@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, dish=dish)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'restaurant/cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Здесь вы можете реализовать логику заказа, например, сохранить данные заказа и очистить корзину
    cart_items.delete()

    return render(request, 'restaurant/checkout.html', {'message': 'Заказ оформлен успешно!'})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})