# voice_comment_views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tasks.models import Upload

from django.contrib import messages

# incomplete
@login_required
def voice_comment_views(request, upload_id):
    if request.method == 'POST':
        upload = Upload.objects.get(id=upload_id)
        comments = request.POST.get('comments')  # Assuming 'comments' is the name of your form field
        if comments is not None:
            try:
                upload.comments = comments  # Update the comments attribute of the correct Upload object
                upload.save()
                messages.success(request, 'Comments saved successfully.')
                return redirect('filelist')  # Redirect after saving comments
            except Upload.DoesNotExist:
                messages.error(request, 'Upload not found.')
    return redirect('filelist')