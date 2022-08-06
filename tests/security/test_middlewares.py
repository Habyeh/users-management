"""Test APILoggerMiddleware."""

# Utilities
from tests.utilities.base_test import BaseTest
from faker import Faker
from datetime import datetime, timedelta

# Models
from api.security.models import APIRequestLog

fake = Faker()

class TestAPIRequestLogMiddleware(BaseTest):
    """
    Test API Request Log Middleware.
    """

    def test_request_log_logged_user(self, db, user_data):
        """
        Test API Request Logging with an authenticated user.
        """
        # Signup new user
        self.url = self._get_signup_url()
        self._make_post_request(user_data)

        # Login new user
        self.url = self._get_login_url()
        data = self._get_login_data(user_data)
        self._make_post_request(data)

        # Recover access token
        token = self.response.json()['access']
        n = 3

        # Make 'n' requests with token authentication
        for i in range(0, n):
            format = '%Y-%m-%d'
            i_date = datetime.now().date() - timedelta(days=2)
            initial_date = datetime.strftime(i_date, format)

            f_date = datetime.now().date()
            final_date = datetime.strftime(f_date, format)

            self.url = self._get_date_difference_url(initial_date, final_date)
            headers = {'Authorization': f'Bearer {token}'}
            self._make_get_request(headers)
        
        # Check logs
        requests = APIRequestLog.objects.filter(username=user_data['username'])

        assert requests.exists() == True
        assert requests.count() == n
    
    def test_request_log_anon_user(self, db, user_data):
        """
        Test API Request Logging with an anonymous user.
        """
        n = 3

        for i in range(0, n):
            user_data['username'] = fake.user_name()
            self.url = self._get_signup_url()
            self._make_post_request(user_data)
        
        # Check logs
        requests = APIRequestLog.objects.filter(username='Anonymous')

        assert requests.exists() == True
        assert requests.count() == n