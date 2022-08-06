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

# Utilities
from api.utilities.date_difference_api import DateDifferenceCalculatorApiView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Users
    path('users/', include(('api.users.urls', 'users'), namespace='users')),

    # Security
    path('security/', include(('api.security.urls', 'security'), namespace='security')),

    # Utilities
    path('difference/<str:initial_date>/<str:final_date>/', DateDifferenceCalculatorApiView.as_view(), name='date-difference'),
]
