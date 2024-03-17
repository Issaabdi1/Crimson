# rename_upload_view.py
from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.models import Upload
from django.contrib.auth.decorators import login_required


@login_required
def rename_upload_view(request, upload_id):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        upload = Upload.objects.get(id=upload_id)
        current_name = upload.file.name.split('/')[-1]

        if new_name == current_name:
            messages.error(request, "The new name must be different from the current name.")
        else:
            existing_upload = Upload.objects.filter(file__endswith=new_name).first()
            if existing_upload:
                messages.error(request, "File with this name already exists.")
            else:
                upload.rename_file(new_name)
                messages.success(request, "File renamed successfully.")
    return redirect('filelist')
