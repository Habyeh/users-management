# Serializers
from api.users.serializers import (
    UserLoginSerializer,
    UserSignupSerializer
)


class LoginSerializerErrors:
    USERNAME_MAX = UserLoginSerializer().get_fields()['username'].max_length
    USERNAME_MIN = UserLoginSerializer().get_fields()['username'].min_length
    PASSWORD_MAX = UserLoginSerializer().get_fields()['password'].max_length
    PASSWORD_MIN = UserLoginSerializer().get_fields()['password'].min_length

    USERNAME_MAX_LENGTH = f"Ensure this field has no more than {USERNAME_MAX} characters."
    USERNAME_MIN_LENGTH = f"Ensure this field has at least {USERNAME_MIN} characters."
    PASSWORD_MAX_LENGTH = f"Ensure this field has no more than {PASSWORD_MAX} characters."
    PASSWORD_MIN_LENGTH = f"Ensure this field has at least {PASSWORD_MIN} characters."
    INVALID_CREDENTIALS = "Invalid credentials."
    BLANK_FIELD = 'This field may not be blank.'


class SignupSerializerErrors:
    USERNAME_MAX = UserSignupSerializer().get_fields()['username'].max_length
    USERNAME_MIN = UserSignupSerializer().get_fields()['username'].min_length

    PASSWORD_MAX = UserSignupSerializer().get_fields()['password'].max_length
    PASSWORD_MIN = UserSignupSerializer().get_fields()['password'].min_length

    FIRST_NAME_MAX = UserSignupSerializer().get_fields()['first_name'].max_length
    LAST_NAME_MAX = UserSignupSerializer().get_fields()['last_name'].max_length

    BLANK_FIELD = 'This field may not be blank.'
    PASSWORDS_DISMATCH = "Passwords don't match."
    PASSWORD_MIN_LENGTH = f"Ensure this field has at least {PASSWORD_MIN} characters."
    PASSWORD_MAX_LENGTH = f"Ensure this field has no more than {PASSWORD_MAX} characters."
    FIRST_NAME_MAX_LENGTH = f"Ensure this field has no more than {FIRST_NAME_MAX} characters."
    LAST_NAME_MAX_LENGTH = f"Ensure this field has no more than {LAST_NAME_MAX} characters."