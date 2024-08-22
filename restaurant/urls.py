from django.urls import path
from . import views

urlpatterns = [
    path('', views.DishListView.as_view(), name='menu_list'),
    path('<int:id>/', views.menu_detail, name='menu_detail'),
    path('cart/', views.view_cart, name='view_cart'),  # просмотр корзины
    path('cart/add/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),  # добавление в корзину
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # удаление из корзины
    path('checkout/', views.checkout, name='checkout'),  # оформление заказа
    path('orders/', views.order_history, name='order_history'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('orders/repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
]