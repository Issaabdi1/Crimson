from django.db import models
from .user import User
from task_manager.storage_backends import MediaStorage
from django.core.validators import FileExtensionValidator


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