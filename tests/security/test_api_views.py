"""Test APIRequestLogApiView."""

# Django REST Framework
from rest_framework import status

# Utilities
from tests.utilities.base_test import BaseTest
from faker import Faker
from datetime import datetime, timedelta

# Serializers
from api.security.serializers import APIRequestLogSerializer

fake = Faker()

class TestAPIRequestLogApiView(BaseTest):
    """
    Test API Request Log API View.
    """

    def test_request_log_user(self, db, user_data):
        """
        Test API Request Logging with an authenticated user.
        """
        headers = self._get_auth_token(user_data)

        n = 3

        # Make 'n' requests with token authentication
        for i in range(0, n):
            format = '%Y-%m-%d'
            i_date = datetime.now().date() - timedelta(days=2)
            initial_date = datetime.strftime(i_date, format)

            f_date = datetime.now().date()
            final_date = datetime.strftime(f_date, format)

            self.url = self._get_date_difference_url(initial_date, final_date)
            self._make_get_request(headers)
        
        # Check logs
        self.url = self._get_request_log_url(user_data['username'])
        self._make_get_request(headers)

        assert self.response.status_code == status.HTTP_200_OK
        assert len(self.response.json()) == n
        assert [field for field in self.response.json()[0].keys()] == [field for field in APIRequestLogSerializer().get_fields()]
    
    def test_request_log_not_auth_user(self, db, user_data):
        """
        Test API Request Logging with an anonymous user.
        """
        headers = self._get_auth_token(user_data)

        # Check logs
        self.url = self._get_request_log_url('Anonymous')
        self._make_get_request(headers)

        assert self.response.status_code == status.HTTP_200_OK
        assert len(self.response.json()) == 2