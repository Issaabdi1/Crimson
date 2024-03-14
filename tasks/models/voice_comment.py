from django.db import models
from .user import User
from .upload import Upload
import secrets, string

def random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def user_directory_path(instance, filename):
    random_str = random_string(6)
    return '{0}/{1}/voice_comment_{2}'.format(instance.user.username, instance.upload.file.name, random_str)

class VoiceComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, blank=False)
    mark_id = models.IntegerField(null=True)
    audio = models.FileField(upload_to=user_directory_path, blank=False)