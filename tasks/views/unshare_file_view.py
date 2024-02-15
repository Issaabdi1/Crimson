"""Unsharing files view"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from tasks.models import User, Upload, SharedFiles

@login_required
def unshare_file(request, upload_id, user_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        upload = Upload.objects.get(pk=upload_id)
        shared_file = SharedFiles.objects.get(shared_file=upload)
        shared_file.shared_to.remove(user)
    return redirect('filelist')