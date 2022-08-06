"""Security URLs"""

# Django
from django.urls import path

# Views
from api.security.views import (
    APIRequestLogApiView
)


urlpatterns = [
    path('logs/<str:username>/', APIRequestLogApiView.as_view(), name='logs'),
]