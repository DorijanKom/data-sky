from django.db import models
from django.utils import timezone

from services.core.models import User


class Data(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(null=True, max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.file.name)
