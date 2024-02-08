# rename_upload_view.py
import os

from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django.shortcuts import redirect, get_object_or_404

from task_manager.storage_backends import MediaStorage
from tasks.models import Upload


def rename_upload(request, upload_id):
    if request.method == 'POST':
        upload = get_object_or_404(Upload, pk=upload_id, owner=request.user)
        new_name = request.POST.get('new_name').strip()

        if not new_name:
            messages.error(request, 'The new name cannot be empty.')
            return redirect('filelist')

        _, file_extension = os.path.splitext(upload.file.name)
        new_name_with_extension = f"{new_name}{file_extension}"
        storage = MediaStorage()
        old_file_path = upload.file.name
        new_file_path = os.path.join(os.path.dirname(old_file_path), new_name_with_extension)

        existing_files = Upload.objects.filter(file__iexact=new_name_with_extension, owner=request.user)
        if existing_files.exists():
            messages.error(request, 'A file with the new name already exists.')
            return redirect('filelist')

        if storage.exists(old_file_path):
            storage.save(new_file_path, storage.open(old_file_path))
            storage.delete(old_file_path)
            upload.file.name = new_file_path
            upload.save()
            messages.success(request, 'File renamed successfully.')
        else:
            messages.error(request, 'Original file not found.')
            return redirect('filelist')
    else:
        raise PermissionDenied

    return redirect('filelist')
