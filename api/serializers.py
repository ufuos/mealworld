from rest_framework import serializers
from listings.models import Meal, Category
from cart.models import CartItem
from orders.models import Order
from django.contrib.auth.models import User

# ----------------------------------------
# MAIN SERIALIZERS YOU ASKED TO ADD
# ----------------------------------------

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# ----------------------------------------
# TOGGLE SERIALIZERS (Already in your file)
# ----------------------------------------

class MealToggleActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["id", "is_active"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        instance.is_active = not instance.is_active
        instance.save()
        return instance


class CategoryToggleActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "is_active"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        instance.is_active = not instance.is_active
        instance.save()
        return instance


class CartItemToggleActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "is_active"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        instance.is_active = not instance.is_active
        instance.save()
        return instance


class OrderToggleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "status"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        status_flow = ["pending", "processing", "completed"]

        try:
            current_index = status_flow.index(instance.status)
            next_status = status_flow[(current_index + 1) % len(status_flow)]
        except ValueError:
            next_status = "pending"

        instance.status = next_status
        instance.save()
        return instance
