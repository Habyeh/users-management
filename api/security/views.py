"""Security API Views."""

# Django REST Framework
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

# Models
from api.security.models import APIRequestLog

# Serializers
from api.security.serializers import APIRequestLogSerializer


class APIRequestLogApiView(ListAPIView):
    
    model = APIRequestLog
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return queryset object.
        """
        return self.model.objects.filter(username=self.kwargs['username'])