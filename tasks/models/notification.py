from django.db import models
from tasks.models import User, SharedFiles, Upload

class Notification(models.Model):
    """"Model used for storing notifications which will be shown on the sidebar"""
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    shared_file_instance = models.ForeignKey(SharedFiles, blank=True, null=True, on_delete=models.CASCADE)
    time_of_notification = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default = False) 
    notification_message = models.TextField(blank = False)