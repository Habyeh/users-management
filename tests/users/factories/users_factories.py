"""Users module factories."""

# Utilities
import factory
from faker import Faker

# Models
from django.contrib.auth.models import User

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    """User model factory."""
    class Meta:
        model = User

    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    is_staff = fake.boolean()