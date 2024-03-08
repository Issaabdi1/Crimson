from django.db import models
from .user import User
from.upload import Upload
from task_manager.storage_backends import MediaStorage
from django.core.validators import FileExtensionValidator
#from django.core.files.base import ContentFile
import os
import uuid

def user_directory_path(instance, filename):
    storage = instance.soundfile.storage
    upload_name = os.path.splitext(os.path.basename(instance.upload.file.name))[0]
    random_string = str(uuid.uuid4().hex)[:6]
    name, ext = os.path.splitext(filename)

    #will break if there are 2176782336 voice comments made by 1 user for the same pdf file
    while storage.exists('user_{0}/Voice_Comments_for_{1}/{2}'.format(instance.owner.username,upload_name,name + random_string + ext)):
        random_string = str(uuid.uuid4().hex)[:6]

    return 'user_{0}/Voice_Comments_for_{1}_vcom/{2}'.format(instance.owner.username ,upload_name ,name + random_string + ext)


class VoiceComment(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    soundfile = models.FileField(storage=MediaStorage(),
                            upload_to=user_directory_path,)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='soundfile')

    def get_sound_file_path(self):
        return self.soundfile.name