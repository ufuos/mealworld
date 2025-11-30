from rest_framework import serializers
from listings.models import Meal, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'price', 'slug']
        read_only_fields = ['id', 'slug', 'created', 'updated']
