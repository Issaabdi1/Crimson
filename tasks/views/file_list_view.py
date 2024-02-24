"""file list view"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import User, Upload


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

    return render(request, 'filelist.html', context)
