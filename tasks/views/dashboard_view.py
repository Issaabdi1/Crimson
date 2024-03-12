"""Main dashboard view"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.forms import FileForm
from django.core.files.storage import FileSystemStorage
from tasks.models import Upload, User, SharedFiles, Team
from django.core.exceptions import ValidationError


"""Rick Version"""
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


"""Hanson's Version"""
# @login_required
# def dashboard(request):
#     """Display the current user's dashboard."""
#     current_user = request.user
#     image_url = None
#     context = {'user': current_user}
#     form = FileForm(user=current_user)
#     if request.method == 'POST':
#         form = FileForm(request.POST, request.FILES, user=current_user)
#         if form.is_valid():
#             media_file = request.FILES['file']
#             if settings.USE_S3:
#                 try:
#                     upload = form.save(media_file)
#                     image_url = upload.file.url

#                     # Add upload to team files
#                     team_id = request.POST.get("team_id")
#                     if team_id is not None:
#                         team = Team.objects.get(id=team_id)
#                         team.add_upload(upload)

#                 except ValidationError as e:
#                     messages.add_message(request, messages.ERROR, e.message_dict['file'][0])
#             else:
#                 messages.add_message(request, messages.ERROR, f'The Amazon S3 service is not connected.')
#         else:
#             form = FileForm()
#     if image_url:
#         context['image_url'] = image_url
#     context['form'] = form
#     context['shared'] = SharedFiles.objects.filter(shared_to=current_user)
#     return render(request, 'dashboard.html', context)
