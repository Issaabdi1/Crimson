# rename_upload_view.py
from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.models import Upload


def rename_upload_view(request, upload_id):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        upload = Upload.objects.get(id=upload_id)
        current_name = upload.file.name.split('/')[-1]

        if new_name != current_name:
            existing_upload = Upload.objects.filter(file=new_name).first()
            if existing_upload:
                messages.error(request, "File with this name already exists.")
            else:
                try:
                    upload.rename_file(new_name)
                    messages.success(request, "File renamed successfully.")
                except Exception as e:
                    messages.error(request, f"Error renaming file: {str(e)}")
        else:
            messages.error(request, "The new name must be different from the current name.")

    return redirect('filelist')