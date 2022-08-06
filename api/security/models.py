from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class APIRequestLog(models.Model):
    """Logs Django REST Framework API requests"""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    username = models.CharField(
        max_length=120,
        null=True,
        blank=True,
    )
    requested_at = models.DateTimeField(auto_now=True)
    host = models.CharField(max_length=200)
    url_path = models.CharField(
        max_length=200,
        help_text="url path",
    )
    view_method = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    remote_addr = models.CharField(
        max_length=200,
        help_text="remote ip",
    )
    status_code = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "API Request Log"

    def __str__(self):
        return "{} {}".format(self.view_method, self.url_path)