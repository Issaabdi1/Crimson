"""Share file related views"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from tasks.models import User, Upload, SharedFiles, Notification
from datetime import datetime


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
def share_file(request):
    """Display view handling shared files"""
    user = request.user
    all_users = User.objects.exclude(username=user.username)
    uploads = Upload.objects.filter(owner=user)
    if request.method == 'POST':
        file_id = request.POST.get('file-id')
        user_id = request.POST.get('user-id')
        if file_id is not None and user_id is not None:
            shared_file = Upload.objects.get(id=file_id)
            shared_user = User.objects.get(id=user_id)
            entry, created = SharedFiles.objects.get_or_create(
                shared_file=shared_file,
                shared_by=user,
            )

            Notification.objects.create(
                shared_file_instance = entry,
                user = shared_user,
                time_of_notification = datetime.now()
            )
            if (entry.shared_to.contains(shared_user)):
                messages.error(request, 'User has already been shared this file.')
                return redirect('share_file')
            
            entry.shared_to.add(shared_user)
            entry.save()
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