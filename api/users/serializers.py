"""Users serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Django
from django.contrib.auth import (
    authenticate,
    password_validation
)

# Models
from django.contrib.auth.models import User

# OpenAPI
from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
)


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""
    
    class Meta:
        """Meta class."""
        
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

@extend_schema_serializer(
    examples = [
        OpenApiExample(
            'Login example',
            summary='Login example',
            value={
                'username': "str: User's username.",
                'password': "str: User's password."
            },
            request_only=True,
            response_only=False
        ),
        OpenApiExample(
            'Login response',
            summary='Login response example',
            value={
                'user': "dict: User data.",
                'access': "str: Auth token.",
                'refresh': "str: Refresh token."
            },
            request_only=False,
            response_only=True,
        ),
    ]
)
class UserLoginSerializer(serializers.Serializer):
    """User login serializer.
    
    Handle the login request data.
    """
    
    username = serializers.CharField(min_length=4, max_length=20)
    password = serializers.CharField(min_length=8, max_length=30)
    
    def validate(self, data):
        """Check credentials."""
        
        user = authenticate(username=data['username'], password=data['password'])
        
        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        self.context['user'] = user
        return data
        
        
    def create(self, data):
        """Generate access and refresh token."""
        
        token_serializer = TokenObtainPairSerializer(data=data)
        token_serializer.is_valid(raise_exception=True)

        login_data = {
            'user': UserSerializer(self.context['user']).data,
            'access': token_serializer.validated_data['access'],
            'refresh': token_serializer.validated_data['refresh']
        }
        return login_data
    
    
class UserSignupSerializer(serializers.Serializer):
    """User signup serializer.
    
    Handle signup data validation and user creation.
    """
    
    email = serializers.EmailField(
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    
    # Password
    password = serializers.CharField(min_length=8, max_length=30)
    password_confirmation = serializers.CharField(min_length=8, max_length=30)
    
    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)
    
    def validate(self, data):
        """Check passwords match."""
        
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        
        password_validation.validate_password(passwd)
        return data
    
    
    def create(self, data):
        """Handle user creation."""
        
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        user_serializer = UserSerializer(user)

        return user_serializer.data