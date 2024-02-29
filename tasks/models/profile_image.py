from django.db import models
from django.core.exceptions import ValidationError
from . import User


def user_directory_path(instance, filename):
    return '{0}/user_{1}/{2}'.format('profile_image', instance.user.username, filename)


class ProfileImage(models.Model):
    """Model used for storing user profile image.
       A user can have many profile image,
       but can only display one of them at one time."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):
        """A user can only have 5 avatars at one time"""
        if self.pk is None:
            if self.user.profileimage_set.count() >= 5:
                oldest_avatar = self.user.profileimage_set.order_by('id').first()
                oldest_avatar.delete()
        super().save(*args, **kwargs)