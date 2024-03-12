# outer_comment_views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tasks.models import Upload

from django.contrib import messages


@login_required
def outer_comment_views(request, upload_id):
    if request.method == 'POST':
        upload = Upload.objects.get(id=upload_id)
        comments = request.POST.get('comments')  # Get comments field
        if comments is not None:
            try:
                upload.comments = comments
                upload.save()
                messages.success(request, 'Comments saved successfully.')
                return redirect('filelist')
            except Upload.DoesNotExist:
                messages.error(request, 'Upload not found.')
    return redirect('filelist')
