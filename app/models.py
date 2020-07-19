from django.db import models


class Client(models.Model):
    identity = models.CharField(max_length=255, blank=False, null=False)
    count = models.IntegerField(default=0)
