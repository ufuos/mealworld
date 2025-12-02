from django.contrib import admin       # ✅ Import admin
from django.urls import path, include
from rest_framework import routers
from django.shortcuts import redirect

router = routers.DefaultRouter()
# Include your viewsets here if you have any
# router.register(r'example', ExampleViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),                   # Admin URL
    path("api/", include(router.urls)),               # API URLs
    path("", lambda request: redirect("/api/", permanent=False)),  # Redirect root to /api/
]
