from django.urls import path
from .views import (
    MealListCreateView, MealDetailView, MealRetrieveUpdateDestroyView,
    CategoryListCreateView, CartListCreateView, OrderListCreateView
)

urlpatterns = [
    path("meals/", MealListCreateView.as_view(), name="meals"),
    path("meals/<int:id>/", MealDetailView.as_view(), name="meal-detail"),
    
    # New path for RetrieveUpdateDestroyAPIView
    path("meals/manage/<int:id>/", MealRetrieveUpdateDestroyView.as_view(), name="meal-manage"),

    path("categories/", CategoryListCreateView.as_view(), name="categories"),

    path("cart/", CartListCreateView.as_view(), name="cart"),

    path("orders/", OrderListCreateView.as_view(), name="orders"),
]
