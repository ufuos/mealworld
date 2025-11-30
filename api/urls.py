from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.api.urls')),
    path('listings/', include('listings.api.urls')),
    path('orders/', include('orders.api.urls')),
    path('cart/', include('cart.api.urls')),
]
