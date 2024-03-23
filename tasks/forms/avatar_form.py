"""User Avatar Related Forms for the app."""
from django import forms
from tasks.models import ProfileImage


class UploadProfileImageForm(forms.Form):
    """Form for uploading profile image"""
    image = forms.ImageField(label='Profile Image',
                             label_suffix='')
    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, image):
        """Create and Save the user's new avatar."""

        profile_Image = ProfileImage(image=image, user=self.user)
        profile_Image.full_clean()
        profile_Image.save()
        self.user.avatar_url = profile_Image.image.url
        self.user.save()
        return profile_Image


class AvatarForm(forms.Form):
    """Form for updating profile image"""
    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        avatars = self.user.profileimage_set.all()
        profile_image_urls = [(avatars[index].image.url, avatars[index].image.url) for index in range(avatars.count())]
        self.fields['avatar_url'] = forms.ChoiceField(choices=profile_image_urls, widget=forms.RadioSelect)

    def save(self):
        url = self.cleaned_data['avatar_url']
        self.user.avatar_url = url
        self.user.save()
        return url
