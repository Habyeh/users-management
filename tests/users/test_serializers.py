"""Test Users Serializers"""

# Pytest
import pytest

# Serializers
from api.users.serializers import (
    UserSerializer,
    UserSignupSerializer,
    UserLoginSerializer
)

# Utilities
from django.core.validators import validate_email
from faker import Faker
from tests.users.constants.serializers_errors import (
    LoginSerializerErrors,
    SignupSerializerErrors
)

fake = Faker()

class TestUserSerializer:
    """Test User Serializer."""

    serializer_class = UserSerializer

    def test_serializer_fields(self, new_user):
        """Check serializer returning fields."""
        serializer = self.serializer_class(new_user)
        fields = [field for field in serializer.data.keys()]
        expected_fields = [field for field in self.serializer_class().get_fields().keys()]
        assert fields == expected_fields

    def test_output_format(self, new_user):
        """Check serializer fields output format"""
        serializer = self.serializer_class(new_user)

        username = serializer.data.get('username', None)
        first_name = serializer.data.get('first_name', None)
        last_name = serializer.data.get('last_name', None)
        email = serializer.data.get('email', None)
        
        assert username == new_user.username
        assert first_name == new_user.first_name
        assert last_name == new_user.last_name
        assert email == new_user.email

        for value in serializer.data.values():
            assert isinstance(value, str) == True

        assert validate_email(email) == None


class TestUserSignupSerializer:
    """Test User Signup Serializer."""
    
    serializer_class = UserSignupSerializer
    
    def test_user_creation(self, db, user_data):
        """Test a successful user creation."""
        serializer = self.serializer_class(data=user_data)
        assert serializer.is_valid() == True
        new_user_data = serializer.save()
        assert isinstance(new_user_data, dict) == True
    
    def test_unique_constraints(self, db, user_data):
        """Test unique constraint of email and username fields."""
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid()
        serializer.save()

        serializer = self.serializer_class(data=user_data)
        assert serializer.is_valid() == False
        assert serializer.errors['email'][0].code == 'unique'
        assert serializer.errors['username'][0].code == 'unique'

    def test_different_passwords(self, db, user_data):
        """Test failed user creation by passwords dismatch"""
        user_data['password_confirmation'] = 'somepass'
        serializer = self.serializer_class(data=user_data)
        assert serializer.is_valid() == False
        assert serializer.errors['non_field_errors'][0] == SignupSerializerErrors.PASSWORDS_DISMATCH

    def test_password_min_length(self, db, user_data):
        """Test failed user creation by password min length"""
        user_data['password_confirmation'] = 'pass'
        user_data['password'] = user_data['password_confirmation']
        serializer = self.serializer_class(data=user_data)
        assert serializer.is_valid() == False
        assert serializer.errors['password'][0] == SignupSerializerErrors.PASSWORD_MIN_LENGTH

    def test_password_max_length(self, db, user_data):
        """Test failed user creation by password max length"""
        user_data['password_confirmation'] = fake.text()
        user_data['password'] = user_data['password_confirmation']
        serializer = self.serializer_class(data=user_data)
        assert serializer.is_valid() == False
        assert serializer.errors['password'][0] == SignupSerializerErrors.PASSWORD_MAX_LENGTH
        
    def test_names_max_length(self, db, user_data):
        """Test failed user creation by first and last names max length"""
        user_data['first_name'] = fake.text()
        user_data['last_name'] = user_data['first_name']
        serializer = self.serializer_class(data=user_data)
        assert serializer.is_valid() == False
        assert serializer.errors['first_name'][0] == SignupSerializerErrors.FIRST_NAME_MAX_LENGTH
        assert serializer.errors['last_name'][0] == SignupSerializerErrors.LAST_NAME_MAX_LENGTH

    def test_output_fields(self, new_user):
        """Check serializer returning fields."""
        serializer = UserSerializer(new_user)
        fields = [field for field in serializer.data.keys()]
        expected_fields = [field for field in UserSerializer().get_fields().keys()]
        assert fields == expected_fields


class TestUserLoginSerializer:
    """Test User Login Serializer."""
    
    serializer_class = UserLoginSerializer

    def _signup(self, user_data) -> dict:
        signup_serializer = UserSignupSerializer(data=user_data)
        signup_serializer.is_valid()
        return signup_serializer.save()
    
    def _get_login_data(self, user_data) -> dict:
        return {'username': user_data['username'], 'password': user_data['password']}
    
    def _login(self, user_data) -> dict:
        login_data = self._get_login_data(user_data)
        login_serializer = self.serializer_class(data=login_data)
        login_serializer.is_valid()
        return login_serializer.save()

    def test_login_success(self, db, user_data):
        """Test login serializer success."""
        self._signup(user_data)
        login_data = self._get_login_data(user_data)
        login_serializer = self.serializer_class(data=login_data)

        assert login_serializer.is_valid() == True

    def test_login_output(self, db, user_data):
        """Check login serializer output format."""
        self._signup(user_data)
        login_data = self._login(user_data)
        
        assert [key for key in login_data.keys()] == ['user', 'access', 'refresh']
        
        for key in login_data.keys():
            if key == 'user':
                assert isinstance(login_data[key], dict) ==  True
            else:
                assert isinstance(login_data[key], str) ==  True

    def test_username_min_length(self, db, user_data):
        """Test username min length allowed"""
        login_data = self._get_login_data(user_data)
        login_data['username'] = 'dd'
        login_serializer = self.serializer_class(data=login_data)
        assert login_serializer.is_valid() == False
        assert login_serializer.errors['username'][0] == LoginSerializerErrors.USERNAME_MIN_LENGTH

    def test_username_max_length(self, db, user_data):
        """Test username max length allowed"""
        login_data = self._get_login_data(user_data)
        login_data['username'] = fake.text()
        login_serializer = self.serializer_class(data=login_data)
        assert login_serializer.is_valid() == False
        assert login_serializer.errors['username'][0] == LoginSerializerErrors.USERNAME_MAX_LENGTH

    def test_password_min_length(self, db, user_data):
        """Test password min length allowed"""
        login_data = self._get_login_data(user_data)
        login_data['password'] = 'dd'
        login_serializer = self.serializer_class(data=login_data)
        assert login_serializer.is_valid() == False
        assert login_serializer.errors['password'][0] == LoginSerializerErrors.PASSWORD_MIN_LENGTH

    def test_password_max_length(self, db, user_data):
        """Test password max length allowed"""
        login_data = self._get_login_data(user_data)
        login_data['password'] = fake.text()
        login_serializer = self.serializer_class(data=login_data)
        assert login_serializer.is_valid() == False
        assert login_serializer.errors['password'][0] == LoginSerializerErrors.PASSWORD_MAX_LENGTH

    def test_invalid_credentials(self, db, user_data):
        """Test login with invalid credentials"""
        self._signup(user_data)
        user_data['password']=fake.password()
        login_data = self._get_login_data(user_data)
        login_serializer = self.serializer_class(data=login_data)
        assert login_serializer.is_valid() == False
        assert login_serializer.errors['non_field_errors'][0] == LoginSerializerErrors.INVALID_CREDENTIALS