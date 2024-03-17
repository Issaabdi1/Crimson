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
    upload_form = UploadProfileImageForm(user=current_user)
    avatar_form = AvatarForm(user=current_user)
    profile_form = UserForm(instance=request.user)

    if request.method == 'POST':
        if 'upload_image' in request.POST:
            upload_form = UploadProfileImageForm(request.POST, request.FILES, user=current_user)
            handle_upload_image(request, current_user, upload_form)
        elif 'update_avatar' in request.POST:
            avatar_form = AvatarForm(request.POST, user=current_user)
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
    if upload_form.is_valid():
        image = request.FILES['image']
        if settings.USE_S3:
            upload_form.save(image=image)
            messages.success(request, "Image uploaded successfully!")
        else:
            messages.add_message(request, messages.ERROR, 'The Amazon S3 service is not connected.')
    else:
        messages.add_message(request, messages.ERROR, 'Image upload unsuccessfully.')


def handle_update_avatar(request, current_user, avatar_form):
    """Handle the update avatar form submission."""
    if avatar_form.is_valid():
        avatar_form.save()
        messages.success(request, "Avatar updated successfully!")
    else:
        messages.add_message(request, messages.ERROR, 'Avatar update unsuccessfully.')
