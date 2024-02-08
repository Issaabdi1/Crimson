from django.db import models
from tasks.models import User, SharedFiles

class Notification(models.Model):
    """"Model used for storing notifications which will be shown on the sidebar"""
    shared_file_instance = models.ForeignKey(SharedFiles, on_delete=models.CASCADE)
    time_of_notification = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)