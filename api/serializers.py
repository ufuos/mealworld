from rest_framework import serializers
from django.contrib.auth.models import User
from listings.models import Meal, Category
from cart.models import CartItem
from orders.models import Order


class MealWorldSerializer(serializers.Serializer):
    # User fields
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    # Meal fields
    meal_id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    price = serializers.DecimalField(required=False, max_digits=8, decimal_places=2)
    category = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    description = serializers.CharField(required=False)

    # Category fields
    category_id = serializers.IntegerField(required=False)
    category_name = serializers.CharField(required=False)
    category_slug = serializers.CharField(required=False)

    # Cart fields
    cart_item_id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False)

    # Order fields
    order_id = serializers.IntegerField(required=False)
    total_amount = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    status = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)

    def to_representation(self, instance):
        """Dynamically detect instance type and serialize."""
        data = {}

        if isinstance(instance, User):
            data.update({
                "id": instance.id,
                "username": instance.username,
                "email": instance.email
            })

        elif isinstance(instance, Category):
            data.update({
                "category_id": instance.id,
                "category_name": instance.name,
                "category_slug": instance.slug
            })

        elif isinstance(instance, Meal):
            data.update({
                "meal_id": instance.id,
                "title": instance.title,
                "price": instance.price,
                "category": instance.category.name,
                "image": instance.image.url if instance.image else None,
                "description": instance.description
            })

        elif isinstance(instance, CartItem):
            data.update({
                "cart_item_id": instance.id,
                "meal": MealWorldSerializer(instance.meal).data,
                "quantity": instance.quantity
            })

        elif isinstance(instance, Order):
            data.update({
                "order_id": instance.id,
                "total_amount": instance.total_amount,
                "status": instance.status,
                "created_at": instance.created_at
            })

        return data
