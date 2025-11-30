from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from orders.models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "id"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'transport']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['created', 'updated']
    ordering = ['-created']

    def get_queryset(self):
        """
        Prevent Swagger / DRF Spectacular schema errors.
        Ensures AnonymousUser does not trigger a lookup on `id`.
        """
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()

        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(user=user)

        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
