"""Main dashboard view"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import Upload, User


@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    current_user = request.user
    uploads = Upload.objects.filter(owner=current_user)
    all_users = User.objects.exclude(username=current_user.username)

    row_number = 1
    for upload in uploads:
        upload.file_size_mb = upload.get_file_size_mb()
        upload.simple_file_name = upload.get_simple_file_name()

    context = {'uploads': uploads,
               'user': current_user,
               "all_users": all_users,
               "row_number": row_number,
               }
    return render(request, 'dashboard.html', context)