from django.conf import settings
from django.db import models
from django.utils import timezone

from services.core.models import Directory


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    file = models.FileField()
    date_created = models.DateTimeField(default=timezone.now)
    size = models.CharField()

    def __str__(self):
        return str(self.file.name)
