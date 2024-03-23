"""Main dashboard view"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from tasks.models import Upload, User
from django.core.paginator import Paginator
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.http import require_POST
import io
import zipfile


@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    current_user = request.user
    uploads = Upload.objects.filter(owner=current_user)
    all_users = User.objects.exclude(username=current_user.username)

    page_number = request.GET.get('page', 1)
    per_page = 7
    paginator = Paginator(uploads, per_page)
    page_obj = paginator.get_page(page_number)

    row_number = (int(page_number) - 1) * per_page
    for upload in page_obj.object_list:
        upload.file_size_mb = upload.get_file_size_mb()
        upload.simple_file_name = upload.get_simple_file_name()
        row_number += 1
        upload.row_id = row_number

    context = {'uploads': page_obj.object_list,
               'user': current_user,
               "all_users": all_users,
               "row_number": row_number,
               "paginator": paginator,
               "current_page": paginator.page(page_number),
               "last_three_page": paginator.num_pages - 2,
               "last_few_pages": paginator.num_pages - 4,
               "next_few_page": int(page_number) + 3,
               }
    return render(request, 'dashboard.html', context)


@login_required
def download_single(request, upload_id):
    # Retrieve the Upload object
    upload = get_object_or_404(Upload, id=upload_id, owner=request.user)
    # Access the file's content directly from storage
    file_content = upload.file.read()
    # Create an HTTP response with the file content, MIME type, and suggested file name
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{upload.file.name}"'
    return response


@login_required
def download_multiple(request):
    if request.method != "POST":
        return JsonResponse({'error': 'This method is not allowed'}, status=405)

    data = json.loads(request.body)
    upload_ids = data.get('upload_ids', [])

    if not upload_ids:
        return JsonResponse({'error': 'No upload IDs provided'}, status=400)

    # Initialize an in-memory zip file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for upload_id in upload_ids:
            upload = get_object_or_404(Upload, id=upload_id, owner=request.user)
            zip_file.writestr(upload.file.name, upload.file.read())

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="uploads.zip"'
    return response


@login_required
@require_POST
def delete_selected_uploads(request):
    data = json.loads(request.body)
    upload_ids = data.get('upload_ids', [])

    # Filter uploads to ensure they belong to the user
    uploads_to_delete = Upload.objects.filter(id__in=upload_ids, owner=request.user)

    for upload in uploads_to_delete:
        upload.file.delete()  # This deletes the file from storage
        upload.delete()  # This deletes the Upload record from the database

    return JsonResponse({'status': 'success'})
