from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('<int:id>/', views.menu_detail, name='menu_detail'),
]