# Django REST Framework
from rest_framework import status

# Pytest
import pytest

# Config
from django.conf import settings

# Utilities
from faker import Faker
from tests.users.constants.serializers_errors import (
    LoginSerializerErrors,
    SignupSerializerErrors
)
from tests.utilities.base_test import BaseTest

# Models
from django.contrib.auth.models import User

# Serializers
from api.users.serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    UserSerializer
)

fake = Faker()

class TestUserAuthViewSet(BaseTest):
    """
    Manage all UserAuthViewSet tests.
    Tests signup, login and logout actions of the
    API considering many cases.
    """

    def test_success_signup(self, db, user_data):
        """
        Test a successful signup case.
        """
        self.url = self._get_signup_url()
        self._make_post_request(user_data)
        fields = [field for field in self.response.json().keys()]
        expected_fields = [field for field in UserSerializer().get_fields().keys()]

        assert self.response.status_code == status.HTTP_201_CREATED
        assert fields == expected_fields
        assert User.objects.filter(username=user_data['username']).exists() == True

    @pytest.mark.parametrize(
        'field, value, response, error',
        [
            ('username', '', 'username', SignupSerializerErrors.BLANK_FIELD),                               # Blank username
            ('password', fake.password(), 'non_field_errors', SignupSerializerErrors.PASSWORDS_DISMATCH),   # Passwords dismatch
            ('password', 'pass', 'password', SignupSerializerErrors.PASSWORD_MIN_LENGTH),                   # Password too small
            ('password', fake.text(), 'password', SignupSerializerErrors.PASSWORD_MAX_LENGTH),              # Password too large
            ('first_name', fake.text(), 'first_name', SignupSerializerErrors.FIRST_NAME_MAX_LENGTH),        # First name too large
            ('last_name', fake.text(), 'last_name', SignupSerializerErrors.LAST_NAME_MAX_LENGTH)            # Last name too large
        ]
    )
    def test_failed_signup(self, db, user_data, field,
                           response, value, error):
        """
        Test signup fail in many cases:
        - Blank username
        - Passwords dismatch.
        - Password too small
        - Password too large
        - First name too large
        - Last name too large
        """
        self.url = self._get_signup_url()
        user_data[field] = value
        self._make_post_request(user_data)
        assert self.response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.response.json()[response][0] == error
    
    def test_login_success(self, db, user_data):
        """
        Test login success case.
        Login proccess should return user data, access and refresh tokens.
        """
        self.url = self._get_signup_url()
        self._make_post_request(user_data)

        self.url = self._get_login_url()
        
        data = self._get_login_data(user_data)
        self._make_post_request(data)

        expected_response_fields = ['user', 'access', 'refresh']
        assert self.response.status_code == status.HTTP_200_OK
        assert [field for field in self.response.json().keys()] == expected_response_fields

    @pytest.mark.parametrize(
        'field, value, error',
        [
            ('username', '', LoginSerializerErrors.BLANK_FIELD),
            ('password', '', LoginSerializerErrors.BLANK_FIELD),
        ]
    )
    def test_login_fail_blank_fields(self, db, user_data,
                        field, value, error):
        """
        Test login fail case by password dismatch.
        """
        self.url = self._get_signup_url()
        self._make_post_request(user_data)

        self.url = self._get_login_url()
        user_data[field] = value
        data = self._get_login_data(user_data)
        self._make_post_request(data)

        assert self.response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.response.json()[field][0] == error

    
    @pytest.mark.parametrize(
        'field, value, key, error',
        [
            ('username', 'u', 'username', LoginSerializerErrors.USERNAME_MIN_LENGTH),
            ('username', fake.text(), 'username', LoginSerializerErrors.USERNAME_MAX_LENGTH),
            ('password', 'u', 'password', LoginSerializerErrors.PASSWORD_MIN_LENGTH),
            ('password', fake.text(), 'password', LoginSerializerErrors.PASSWORD_MAX_LENGTH),
            ('password', 'somefakepass', 'non_field_errors', LoginSerializerErrors.INVALID_CREDENTIALS)
        ]
    )
    def test_login_fail(self, db, user_data, key,
                        field, value, error):
        """
        Test login fail case by many cases.
        - Username min length
        - Username max length
        - Password min length
        - Password max length
        - Invalid credentials
        """
        self.url = self._get_signup_url()
        self._make_post_request(user_data)

        self.url = self._get_login_url()
        user_data[field] = value
        data = self._get_login_data(user_data)
        self._make_post_request(data)

        assert self.response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.response.json()[key][0] == error
    
    def test_success_logout(self, db, user_data):
        """
        Test user logout.
        """
        headers = self._get_auth_token(user_data)
        self.url = self._get_logout_url()
        self._make_post_request(None,headers)

        assert self.response.status_code == status.HTTP_200_OK

    def test_fail_logout(self, db, user_data):
        """
        Test failing user logout.
        """
        headers = self._get_auth_token(user_data)
        headers['Authorization'] = fake.uuid4()
        self.url = self._get_logout_url()
        self._make_post_request(None,headers)
        
        assert self.response.status_code == status.HTTP_401_UNAUTHORIZED