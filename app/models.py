from django.db import models


class ClientRequestLog(models.Model):
    identity = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
