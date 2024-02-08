"""file list view"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import User, Upload, Notification


@login_required
def filelist(request):
    """Display the current user's uploaded files."""

    current_user = request.user
    all_users = User.objects.all()
    notifications = list(reversed(Notification.objects.filter(user = current_user)))
    uploads = Upload.objects.filter(owner=current_user)
    context = {'uploads': uploads,
               'user': current_user,
               "all_users": all_users,
               'notifications' : notifications,
    }

    return render(request, 'filelist.html', context)