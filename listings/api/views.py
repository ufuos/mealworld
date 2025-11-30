from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from listings.models import Meal
from .serializers import MealSerializer

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created']
    ordering = ['-created']
