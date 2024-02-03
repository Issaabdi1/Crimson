from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, FileForm
from tasks.helpers import login_prohibited
from django.core.files.storage import FileSystemStorage
from tasks.models import User, Upload, SharedFiles

@login_required
def shared_file_list(request):
    """Display the current user's shared files."""

    current_user = request.user
    shared_files = SharedFiles.objects.filter(shared_to=current_user)
    context = {'shared_files': shared_files,
               'user': current_user,
               }
    return render(request, 'shared_file_list.html', context)

@login_required
def filelist(request):
    """Display the current user's uploaded files."""

    current_user = request.user
    uploads = Upload.objects.filter(owner=current_user)
    context = {'uploads': uploads,
               'user': current_user,
               }
    return render(request, 'filelist.html', context)

@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    context = {'user': current_user}
    form = FileForm()
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            media_file = request.FILES['file']
            if settings.USE_S3:
                upload = Upload(file=media_file, owner=current_user)
                upload.save()
                image_url = upload.file.url
            else:
                fs = FileSystemStorage()
                filename = fs.save(media_file.name, media_file)
                image_url = fs.url(filename)
                upload = Upload(file=filename, owner=current_user)
                upload.save()
            context['image_url'] = image_url
        else:
            form = FileForm()
    context['form'] = form
    context['shared'] = SharedFiles.objects.filter(shared_to=current_user)
    return render(request, 'dashboard.html', context)


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')

@login_required
def share_file(request):
    """Display form handling shared files"""
    user = request.user
    all_users = User.objects.all()
    uploads = Upload.objects.filter(owner=user)

    if request.method == 'POST':
        file_id = request.POST.get('file-id')
        user_id = request.POST.get('user-id')

        if file_id is not None and user_id is not None:
            shared_file = Upload.objects.get(id=file_id)
            shared_user = User.objects.get(id=user_id)
            SharedFiles.objects.create(
                shared_file=shared_file.file,
                shared_by=user,
                shared_to=shared_user
            )
            return redirect('dashboard')
        else:
            messages.error(request, 'File and user must be selected.')

    if not uploads.exists():
        messages.warning(request, 'You must upload a file before sharing.') 

    context = {
        'uploads': uploads,
        'all_users': all_users,
    }
    return render(request, 'share_file.html', context)


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


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