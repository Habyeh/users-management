# Django REST Framework
from rest_framework import serializers

# Models
from api.security.models import APIRequestLog

class APIRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequestLog
        fields = '__all__'