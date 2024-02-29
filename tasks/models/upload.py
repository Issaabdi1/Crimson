from django.db import models
from .user import User
from task_manager.storage_backends import MediaStorage
from django.core.validators import FileExtensionValidator
from django.core.files.base import ContentFile

import os


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.owner.username, filename)


class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=MediaStorage(),
                            upload_to=user_directory_path,
                            validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                               message='Only files with the extension .pdf are supported.')]
                            )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    comments = models.TextField(blank=True, null=True, default="")

    class Meta:
        """Model options."""

        ordering = ["uploaded_at"]

    def get_shared_users(self):
        """Returns a query set of all the users who have been shared this file"""

        if self.sharedfiles_set.exists():
            return self.sharedfiles_set.all()[0].shared_to.all()
        else:
            return None

    def get_shared_teams(self):
        """Returns a query set of all the teams who have been shared this file"""

        if self.team_set.exists():
            return self.team_set.all()
        else:
            return None
        
    def rename_file(self, new_name):
        storage = self.file.storage

        with storage.open(self.file.name) as f:
            content = f.read()

        current_path, current_filename = os.path.split(self.file.name)
        new_filename, current_extension = os.path.splitext(current_filename)

        new_filename = new_name + current_extension
        new_path = os.path.join(current_path, new_filename)

        if storage.exists(new_path):
            raise ValueError("File with this name already exists.")

        new_file = ContentFile(content)
        storage.save(new_path, new_file)

        self.file.name = new_path
        self.save()
