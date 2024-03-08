"""PDF Viewer view"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from tasks.models import Upload

@login_required
def viewer(request):
    """Displays the PDF in the custom PDF viewer"""

    current_user = request.user
    context = {"user": current_user}
    if request.method == "POST":
        upload_id = request.POST.get('upload_id')
        # Check if the 'upload_id' is present in the form data
        if upload_id is not None:
            try:
                upload = Upload.objects.get(id=upload_id)
                context['upload'] = upload
            except Upload.DoesNotExist:
                messages.add_message(request, messages.ERROR, "Upload does not exist!")
        else:
            messages.add_message(request, messages.ERROR, f'Upload id was not specified in the form!')

    return render(request, 'viewer.html', context)