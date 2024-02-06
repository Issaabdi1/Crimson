from django.db import models
from .user import User
from task_manager.storage_backends import MediaStorage

class SharedFiles(models.Model):
    """"Model used for storing files shared between users"""
    shared_file = models.FileField(storage=MediaStorage())
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="by")
    shared_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to")

    # Share date = models.DateTimeField(auto_now_add=True)