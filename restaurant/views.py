from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, CartItem, Cart, MenuItem, OrderItem, Order
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.views import LogoutView, LoginView

def home(request):
    return render(request, 'restaurant/home.html')

def menu_list(request):
    query = request.GET.get('search')  # Получаем поисковый запрос из GET-параметра
    if query:
        # Ищем блюда, название которых содержит поисковый запрос (без учета регистра)
        items = MenuItem.objects.filter(Q(name__icontains=query))
    else:
        # Если запрос пуст, показываем все блюда
        items = MenuItem.objects.all()
    return render(request, 'restaurant/menu_list.html', {'dishes': items})

def menu_detail(request, id):
    item = get_object_or_404(MenuItem, id=id)
    return render(request, 'restaurant/menu_detail.html')

class DishListView(ListView):
    model = Dish
    template_name = "restaurant/menu_list.html"

    def get_queryset(self): # новый
        query= self.request.GET.get('q')
        if not query:
            query = ''
        object_list = Dish.objects.filter(
            Q(name__icontains=query)
        )
        return object_list

@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Получаем существующий CartItem или создаем новый
    cart_item, created = CartItem.objects.get_or_create(cart=cart, dish=dish)
    
    # Если объект был создан, он имеет значение created = True
    if not created:
        # Если объект уже существует, увеличиваем количество
        cart_item.quantity += 1
    else:
        # Если объект был только что создан, устанавливаем количество в 1
        cart_item.quantity = 1
    
    cart_item.save()

    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Рассчитать общее количество блюд
    total_items = sum(item.quantity for item in cart_items)
    
    # Рассчитать общую стоимость
    total_price = sum(item.quantity * item.dish.price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price
    }
    
    return render(request, 'restaurant/cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if cart_items.exists():
        total_price = sum(item.quantity * item.dish.price for item in cart_items)
        
        # Создаем заказ
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Переносим товары из корзины в заказ
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                dish=item.dish,
                quantity=item.quantity,
                price=item.dish.price
            )

        # Очищаем корзину
        cart_items.delete()

        return render(request, 'restaurant/checkout.html', {'message': 'Заказ оформлен успешно!'})

    return redirect('view_cart')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'restaurant/order_history.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def update_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    # Обрабатываем каждый элемент корзины
    for item in CartItem.objects.filter(cart=cart):
        quantity = request.POST.get(f'quantity_{item.id}', 0)
        if quantity.isdigit() and int(quantity) > 0:
            item.quantity = int(quantity)
            item.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def repeat_order(request, order_id):
    # Получаем заказ по ID
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Создаем новый заказ на основе предыдущего
    new_order = Order.objects.create(user=request.user, total_price=order.total_price)
    
    # Копируем товары из старого заказа в новый
    for item in OrderItem.objects.filter(order=order):
        OrderItem.objects.create(
            order=new_order,
            dish=item.dish,
            quantity=item.quantity,
            price=item.price
        )
    
    # Перенаправляем на страницу оформления заказа
    return redirect('view_cart')

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "login"