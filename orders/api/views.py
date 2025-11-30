from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from orders.models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'transport']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['created', 'updated']
    ordering = ['-created']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
