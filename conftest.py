# Pytest
import pytest

# Factoryboy
from pytest_factoryboy import register
from tests.users.factories.users_factories import UserFactory
from faker import Faker

register(UserFactory)


@pytest.fixture
def new_user(db, user_factory):
    return user_factory.create()

@pytest.fixture
def user_data():
    fake = Faker()
    password = fake.password()
    user_data = {
        'username': fake.user_name(),
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password': password,
        'password_confirmation': password
    }
    return user_data