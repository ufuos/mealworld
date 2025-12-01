from rest_framework import generics, permissions
from .serializers import MealWorldSerializer
from listings.models import Meal, Category
from cart.models import CartItem
from orders.models import Order
from django.contrib.auth.models import User


class MealListView(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealWorldSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Optionally associate a user if meals are user-specific
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class MealDetailView(generics.RetrieveAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealWorldSerializer
    lookup_field = "id"


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = MealWorldSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Categories may not need a user, adjust if needed
        serializer.save()


class CartListView(generics.ListCreateAPIView):
    serializer_class = MealWorldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderListView(generics.ListCreateAPIView):
    serializer_class = MealWorldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Create your views here.
