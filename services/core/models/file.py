from django.db import models
from django.utils import timezone

from services.core.models import User, Directory


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    file = models.FileField(null=True, max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.file.name)
