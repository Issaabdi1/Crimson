from django.db import models
from .user import User
from .upload import Upload

class SharedFiles(models.Model):
    """"Model used for storing files shared between users"""
    shared_file = models.ForeignKey(Upload, on_delete=models.CASCADE, blank=False)
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="by")
    shared_to = models.ManyToManyField(User, related_name="to", blank=True)
    date = models.DateTimeField(auto_now_add=True)
