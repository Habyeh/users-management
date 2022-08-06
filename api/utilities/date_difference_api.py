"""Date Difference API View"""

# Django REST Framework
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Utilities
from datetime import datetime

# OpenAPI
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)


@extend_schema_view(
    get=extend_schema(
        tags=['utilities'],
        description="Creates a Thought object with the given data.",
        responses={
            200: OpenApiResponse(
                description="Success.",
            ),
            400: OpenApiResponse(
                description="Bad request",
            )
        }
    )
)
class DateDifferenceCalculatorApiView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        """Return a difference between 2 given dates."""
        if not 'initial_date' in self.kwargs or not 'final_date' in self.kwargs:
            error = 'You should send both initial and final dates to calcule a difference between them.'
            return Response({'error':error}, status=status.HTTP_400_BAD_REQUEST)

        initial_date = self.kwargs['initial_date']
        final_date = self.kwargs['final_date']

        format = '%Y-%m-%d'

        try:
            initial_date = datetime.strptime(initial_date, format).date()
            final_date = datetime.strptime(final_date, format).date()
        except:
            error = 'Dates format should be: %Y-%m-%d'
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        if not final_date > initial_date:
            error = 'initial_date should be less than final_date'
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        difference = (final_date-initial_date).days
        return Response({'difference': f'{difference} days'}, status=status.HTTP_200_OK)