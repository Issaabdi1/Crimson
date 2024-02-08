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

        # Extract the file extension from the original filename
        _, file_extension = os.path.splitext(upload.file.name)

        # Construct the new filename with the file extension
        new_file_name = f"{new_name}{file_extension}"

        # Construct the new file path
        new_file_path = os.path.join(os.path.dirname(upload.file.name), new_file_name)

        # Check if a file with the new name already exists
        if Upload.objects.filter(file=new_file_path).exclude(pk=upload_id).exists():
            messages.error(request, 'A file with the new name already exists.')
            return redirect('filelist')

        storage = MediaStorage()

        # Check if the original file exists
        if storage.exists(upload.file.name):
            try:
                # Save the file with the new name
                with storage.open(upload.file.name) as old_file:
                    storage.save(new_file_path, old_file)

                # Delete the old file
                storage.delete(upload.file.name)

                # Update the upload object with the new file path
                upload.file.name = new_file_path
                upload.save()

                messages.success(request, 'File renamed successfully.')
            except Exception as e:
                messages.error(request, f'Failed to rename file: {str(e)}')
        else:
            messages.error(request, 'Original file not found.')
    else:
        raise PermissionDenied

    return redirect('filelist')
