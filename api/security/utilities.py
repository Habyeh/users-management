"""API Logger Object."""

# Serializers
from api.security.serializers import APIRequestLogSerializer

class APILogger(object):
    """Mixin to log requests"""

    def __init__(self, request, response):
        self.serializer_class = APIRequestLogSerializer
        self.request = request
        self.response = response
        self.sensitive_fields = {}
        self.log = {}

    def start(self):
        self._get_user()
        self._get_url_path()
        self._get_view_method()
        self._get_ip_address()
        self._get_host()
        self._get_status_code()
        self._save_data()

    def _get_user(self) -> None:
        """Add (request) user data to the request log."""
        user = self.request.user
        if not user.is_authenticated:
            self.log['user'] = None
            self.log['username'] = 'Anonymous'
        else:
            self.log['user'] = user.id
            self.log['username'] = user.username

    def _get_host(self) -> None:
        """Add host to request log."""
        self.log['host'] = self.request.get_host()

    def _get_url_path(self) -> None:
        """Add the requested path to the log."""
        self.log['url_path'] = self.request.path

    def _get_view_method(self):
        """Add requested view method to request log."""
        self.log['view_method'] = self.request.method.lower()

    def _get_ip_address(self) -> None:
        """Add the remote ip address the request was generated from
        to request log."""
        ipaddr = self.request.META.get("HTTP_X_FORWARDED_FOR", None)
        if not ipaddr:
            ipaddr = self.request.META.get("REMOTE_ADDR")
        self.log['remote_addr'] = ipaddr

    def _get_status_code(self) -> None:
        """Add status code from view response to request log."""
        self.log['status_code'] = self.response.status_code
    
    def _save_data(self) -> None:
        """Save request log information."""
        serializer = self.serializer_class(data=self.log)
        if serializer.is_valid():
            serializer.save()