from django.db import models
from .user import User
from .upload import Upload

def user_directory_path(instance, filename):
    return '{0}/{1}/voice_comment_{2}'.format(instance.user.username, instance.upload.file.name, instance.pk)

class VoiceComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, blank=False)
    mark_id = models.IntegerField(null=True)
    audio = models.FileField(upload_to=user_directory_path, blank=False)

    