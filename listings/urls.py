# listings/urls.py
from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    # Default meal list (no category)
    path('', views.meal_list, name='meal_list'),

    # Meal list filtered by category
    path(
        'category/<slug:category_slug>/',
        views.meal_list,
        name='meal_by_category'
    ),

    # Meal detail inside category
    path(
        'category/<slug:category_slug>/<slug:meal_slug>/',
        views.meal_detail,
        name='meal_detail'
    ),
]
