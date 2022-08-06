# Utilities
from api.security.utilities import APILogger

class APILoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        logger = APILogger(request,response)
        logger.start()
        return response