from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
import urllib.parse


class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    avatar_url = models.TextField(default=settings.DEFAULT_IMAGE_URL, blank=False)
    theme_preference = models.CharField(max_length=30, default='default-mode')

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""

        return self.gravatar(size=60)

    def save(self, *args, **kwargs):
        """Custom save method to update avatar_url before saving."""
        # Only update the avatar URL if it's the default, or you might want to add additional logic
        if self.avatar_url == settings.DEFAULT_IMAGE_URL:
            self.avatar_url = self.generate_ui_avatar_url()
        super(User, self).save(*args, **kwargs)

    def generate_ui_avatar_url(self):
        """Generate an avatar URL using the UI Avatars API."""
        initials = f"{self.first_name[0]}{self.last_name[0]}".upper()
        # Construct the URL with desired options. Add or modify parameters as needed.
        base_url = "https://ui-avatars.com/api/"
        params = {
            'name': initials,
            'size': '128',  # You can adjust the size
            'background': 'random',
            'font-size': '0.5',  # Adjust font size relative to the image size
            'length': '2'  # Limit the generated text to 2 characters
        }
        url_params = urllib.parse.urlencode(params)
        avatar_url = f"{base_url}?{url_params}"
        return avatar_url
