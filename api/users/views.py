"""Users Authentication API Views."""

# Django REST Framework
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework_simplejwt.tokens import RefreshToken

# Serializers
from api.users.serializers import (
    UserLoginSerializer,
    UserSerializer,
    UserSignupSerializer,
)

# OpenAPI
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)


@extend_schema_view(
    login=extend_schema(
        description="Creates a Thought object with the given data.",
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(
                description="User authenticated successfully.",
                response=UserLoginSerializer
            ),
            400: OpenApiResponse(
                description="Bad request",
            )
        }
    ),
    signup=extend_schema(
        description="User registration.",
        request=UserSignupSerializer,
        responses={
            201: OpenApiResponse(
                description="User registered successfully.",
                response=UserSerializer
            ),
            400: OpenApiResponse(
                description="Bad request",
            )
        },
    ),
    logout=extend_schema(
        description="User logout.",
        responses={
            200: OpenApiResponse(
                description="User logged out."
            ),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            )
        },
    )
)
class UserAuthViewSet(viewsets.GenericViewSet):
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login']:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """User logout."""
        RefreshToken.for_user(request.user)
        return Response({'success':'Session closed.'}, status=status.HTTP_200_OK)