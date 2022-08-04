"""
Users Management API URL Configuration
"""
# Django
from django.contrib import admin
from django.urls import path, include

# DRF Spectacular
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Users
    path('', include(('api.users.urls', 'users'), namespace='users')),
]
