from django.db import models
from .user import User
from task_manager.storage_backends import MediaStorage



class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=MediaStorage())
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    class Meta:
        """Model options."""

        ordering = ["uploaded_at"]