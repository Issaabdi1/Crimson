from django.conf import settings
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

    def delete(self, *args, **kwargs):
        """Override delete method to handle user's profile image"""
        is_using = self.user.avatar_url == self.image.url
        super().delete(*args, **kwargs)
        if self.user.first_name and self.user.last_name:
            initials = f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        elif self.user.first_name:
            initials = f"{self.user.first_name[0]}".upper()
        elif self.user.last_name:
            initials = f"{self.user.last_name[0]}".upper()
        else:
            initials = "AD"
        if is_using:
            if self.user.profileimage_set.count() > 0:
                self.user.avatar_url = self.user.profileimage_set.order_by('id').first().image.url
            else:
                self.user.avatar_url = f'https://ui-avatars.com/api/?name={initials}&size=128&background=random&font-size=0.5&length=2'
            self.user.save()
