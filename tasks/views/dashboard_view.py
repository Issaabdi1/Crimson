"""Main dashboard view"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.forms import FileForm
from django.core.files.storage import FileSystemStorage
from tasks.models import Upload, SharedFiles, Notification
from django.core.exceptions import ValidationError


@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    current_user = request.user
    image_url = None
    context = {'user': current_user}
    notifications = list(reversed(Notification.objects.filter(user = current_user)))
    form = FileForm()
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            media_file = request.FILES['file']
            if settings.USE_S3:
                upload = Upload(file=media_file, owner=current_user)
                try:
                    upload.full_clean()
                    upload.save()
                    image_url = upload.file.url
                except ValidationError as e:
                    messages.add_message(request, messages.ERROR, e.message_dict['file'][0])
            else:
                fs = FileSystemStorage()
                filename = fs.save(media_file.name, media_file)
                upload = Upload(file=filename, owner=current_user)
                try:
                    upload.full_clean()
                    upload.save()
                    image_url = upload.file.url
                except ValidationError as e:
                    messages.add_message(request, messages.ERROR, e.message_dict['file'][0])
        else:
            form = FileForm()
    if image_url:
        context['image_url'] = image_url
    context['form'] = form
    context['shared'] = SharedFiles.objects.filter(shared_to=current_user)
    context['notifications'] = notifications
    return render(request, 'dashboard.html', context)