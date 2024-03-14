"""Forms for the tasks app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Team, ProfileImage, Upload


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username", label_suffix='')
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), label_suffix='')

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label_suffix = ''

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user


class FileForm(forms.Form):

    file = forms.FileField(
        label='Select a File',
        help_text='only files with the extension .pdf are supported, maximum file size allowed is 100 MB.',
        label_suffix=''
    )
    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, file):
        """Save the uploaded file."""

        upload = Upload(file=file, owner=self.user)
        upload.full_clean()
        upload.save()
        return upload

class CreateTeamForm(forms.ModelForm):

    class Meta:
        """Form options."""

        model = Team
        fields = ['name']


class AddUserToTeamForm(forms.Form):
    """Form for adding User to a team"""
    username = forms.CharField(label='Username')


class RenameForm(forms.Form):
    new_name = forms.CharField(label='New file name')


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
