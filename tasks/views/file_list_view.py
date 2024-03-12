"""file list view"""
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import User, Upload
from django.utils import timezone


@login_required
def filelist(request):
    """Display the current user's uploaded files."""

    current_user = request.user
    uploads = Upload.objects.filter(owner=current_user)
    all_users = User.objects.exclude(username=current_user.username)

    context = {'uploads': uploads,
               'user': current_user,
               "all_users": all_users,
    }

    for upload in uploads:
        time_difference = timezone.now() - upload.uploaded_at
        if time_difference.days > 0:
            upload.upload_time_difference = f"{time_difference.days} days ago"
        elif time_difference.seconds < 60:
            upload.upload_time_difference = "just now"
        elif time_difference.seconds < 3600:
            minutes = time_difference.seconds // 60
            upload.upload_time_difference = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            hours = time_difference.seconds // 3600
            upload.upload_time_difference = f"{hours} hour{'s' if hours > 1 else ''} ago"

    response = render(request, 'filelist.html', context)
    response['Refresh'] = '3600'
    return render(request, 'filelist.html', context)


