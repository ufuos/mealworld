from django.urls import path
from .views import (
    MealListCreateView, MealDetail, MealToggleActive,
    CategoryListView, CategoryDetailView, CategoryToggleActive,
    CartListView, CartDetailView, CartItemToggleActive,
    OrderListView, OrderDetailView, OrderToggleStatus
)

urlpatterns = [
    # Meals
    path("meals/", MealListCreateView.as_view(), name="meals"),
    path("meals/<int:id>/", MealDetail.as_view(), name="meal-detail"),
    path("meals/manage/<int:id>/", MealDetail.as_view(), name="meal-manage"),
    path("meals/<int:pk>/toggle-active/", MealToggleActive.as_view(), name="meal-toggle-active"),

    # Categories
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("categories/manage/<int:id>/", CategoryDetailView.as_view(), name="category-manage"),
    path("categories/<int:pk>/toggle-active/", CategoryToggleActive.as_view(), name="category-toggle-active"),

    # Cart
    path("cart/", CartListView.as_view(), name="cart"),
    path("cart/manage/<int:id>/", CartDetailView.as_view(), name="cart-manage"),
    path("cart/<int:pk>/toggle-active/", CartItemToggleActive.as_view(), name="cartitem-toggle-active"),

    # Orders
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/manage/<int:id>/", OrderDetailView.as_view(), name="order-manage"),
    path("orders/<int:pk>/toggle-status/", OrderToggleStatus.as_view(), name="order-toggle-status"),
]
