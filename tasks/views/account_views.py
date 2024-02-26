"""Account related views."""
from typing import Any
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tasks.forms import PasswordForm, UserForm, SignUpForm, UploadProfileImageForm, AvatarForm
from tasks.models import Notification, ProfileImage
from .mixins import LoginProhibitedMixin


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


@login_required
def profile_update_view(request):
    current_user = request.user
    upload_form = UploadProfileImageForm()
    avatar_form = AvatarForm(user=current_user)
    profile_form = UserForm(instance=request.user)

    if request.method == 'POST':
        if 'upload_image' in request.POST:
            handle_upload_image(request, current_user, upload_form)
        elif 'update_avatar' in request.POST:
            handle_update_avatar(request, current_user, avatar_form)
        elif 'update_profile' in request.POST:
            profile_form = UserForm(request.POST, instance=current_user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated!")
                return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)

    context = {
        'user': current_user,
        'upload_form': upload_form,
        'avatar_form': avatar_form,
        'profile_form': profile_form,
    }

    return render(request, "profile.html", context)


def handle_upload_image(request, current_user, upload_form):
    """Handle the upload image form submission."""
    upload_form = UploadProfileImageForm(request.POST, request.FILES)
    if upload_form.is_valid():
        image = request.FILES['image']
        if settings.USE_S3:
            save_image_to_s3(image, current_user)
        else:
            messages.add_message(request, messages.ERROR, 'The Amazon S3 service is not connected.')
    else:
        messages.add_message(request, messages.ERROR, 'Invalid image upload form.')


def handle_update_avatar(request, current_user, avatar_form):
    """Handle the update avatar form submission."""
    avatar_form = AvatarForm(request.POST, user=current_user)
    if avatar_form.is_valid():
        url = avatar_form.clean()['avatar_index']
        current_user.avatar_url = url
        current_user.save()
    else:
        messages.add_message(request, messages.ERROR, 'Invalid avatar update form.')


def save_image_to_s3(image, current_user):
    """Save image to S3 and update current user's avatar URL."""
    new_image = ProfileImage(image=image, user=current_user)
    new_image.full_clean()
    new_image.save()
    current_user.avatar_url = new_image.image.url
    current_user.save()
