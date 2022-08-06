# Django REST Framework
from rest_framework.test import RequestsClient

# Django
from django.urls import reverse

class BaseTest:
    base_url = 'http://localhost:8000'
    client = RequestsClient()
    
    def _get_signup_url(self):
        """
        Return signup url.
        """
        return self.base_url + reverse('users:users-signup')
    
    def _get_login_url(self):
        """
        Return login url.
        """
        return self.base_url + reverse('users:users-login')
    
    def _get_logout_url(self):
        """
        Return logout url.
        """
        return self.base_url + reverse('users:users-logout')
    
    def _get_date_difference_url(self, initial, final):
        """
        Return date difference api url.
        """
        kwargs = {'initial_date':initial, 'final_date':final}
        return self.base_url + reverse('date-difference', kwargs=kwargs)
    
    def _get_request_log_url(self, username):
        """
        Return request log api url.
        """
        kwargs = {'username':username}
        return self.base_url + reverse('security:logs', kwargs=kwargs)
    
    def _make_post_request(self, data, headers=None):
        """
        Make a post request to the server with given data.
        """            
        self.response = self.client.post(self.url,json=data,headers=headers)
        
    def _make_get_request(self, headers=None):
        """
        Make a get request to the server with given data.
        """
        self.response = self.client.get(self.url, headers=headers)
    
    def _get_login_data(self, data):
        """
        Return login data from signup data.
        """
        return {'username': data['username'], 'password': data['password']}
    
    def _get_auth_token(self, user_data):
        """
        Signup and login, then return an access token from user data.
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

        # Set headers
        return {'Authorization': f'Bearer {token}'}