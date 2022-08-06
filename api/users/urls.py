"""Users Auth URLs"""

# Django
from django.urls import path, include

# Views
from api.users.views import (
    UserAuthViewSet
)

# Django REST Framework
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('', UserAuthViewSet, basename='users')

urlpatterns = [
    # Token Refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('', include(router.urls))
]