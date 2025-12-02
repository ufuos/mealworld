from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Required serializers
from .serializers import (
    MealSerializer,
    CategorySerializer,
    CartItemSerializer,
    OrderSerializer
)

# Required models
from listings.models import Meal, Category
from cart.models import CartItem
from orders.models import Order


# =====================================
# MEALS
# =====================================
class MealListCreateView(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    lookup_field = "id"


# Toggle Active Status for Meal
class MealToggleActive(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            meal = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response({"error": "Meal not found"}, status=status.HTTP_404_NOT_FOUND)

        meal.active = not meal.active
        meal.save()
        return Response({"message": "Meal active status toggled", "active": meal.active})


# =====================================
# CATEGORIES
# =====================================
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"


# Toggle Active Status for Category
class CategoryToggleActive(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        category.active = not category.active
        category.save()
        return Response({"message": "Category active status toggled", "active": category.active})


# =====================================
# CART
# =====================================
class CartListView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


# Toggle Active Status for Cart Item
class CartItemToggleActive(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.active = not cart_item.active
        cart_item.save()
        return Response({"message": "Cart item active status toggled", "active": cart_item.active})


# =====================================
# ORDERS
# =====================================
class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# Toggle Order Status
class OrderToggleStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        status_cycle = ["pending", "confirmed", "delivered"]
        current_index = status_cycle.index(order.status)
        new_status = status_cycle[(current_index + 1) % len(status_cycle)]

        order.status = new_status
        order.save()

        return Response({"message": "Order status updated", "status": order.status})
