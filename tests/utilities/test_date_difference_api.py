"""Test DateDifferenceCalculatorApiView"""

# Pytest
import pytest

# Utilities
from tests.utilities.base_test import BaseTest
from datetime import datetime, timedelta

# Django REST Framework
from rest_framework import status


class TestDateDifferenceCalculatorApiView(BaseTest):
    
    @pytest.mark.parametrize(
        'initial_date, final_date, status',
        [
            ('2022-12-12', '2022-12-24', status.HTTP_200_OK),
            ('20221212', '2022-12-24', status.HTTP_400_BAD_REQUEST),
            ('2022-12-12', '20221224', status.HTTP_400_BAD_REQUEST),
            ('2022-12-24', '2022-12-12', status.HTTP_400_BAD_REQUEST)
        ]
    )
    def test_date_difference(self, db, user_data,
                             initial_date, final_date,status):
        """
        Test date difference api in many cases:
        - Success case.
        - Initial date bad format
        - Final date bad format
        - Initial date > final date
        """
        headers = self._get_auth_token(user_data)

        self.url = self._get_date_difference_url(initial_date, final_date)
        self._make_get_request(headers)

        assert self.response.status_code == status