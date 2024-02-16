from django.db import models
from .user import User
from.upload import Upload
from task_manager.storage_backends import MediaStorage
from django.core.validators import FileExtensionValidator
#from django.core.files.base import ContentFile
#import os


def user_directory_path(instance, filename):

    return 'user_{0}/vcom/{1}'.format(instance.owner.username, filename)


class VoiceComment(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    soundfile = models.FileField(storage=MediaStorage(),
                            upload_to=user_directory_path,)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='soundfile')