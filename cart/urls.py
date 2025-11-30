from django.urls import path
from . import views

app_name = "mealworld"   # Updated from finesauses to mealworld

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:meal_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:meal_id>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.cart_clear, name='cart_clear'),
]
