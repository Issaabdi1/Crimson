"""Main dashboard view"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.forms import FileForm
from tasks.models import User, Upload, SharedFiles, Team
from django.core.exceptions import ValidationError


@login_required
def upload_file_view(request):
    current_user = request.user
    file_url = None
    context = {'user': current_user}
    form = FileForm()
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            if 'file' in request.FILES:
                media_file = request.FILES['file']
                if settings.USE_S3:
                    upload = Upload(file=media_file, owner=current_user)
                    try:
                        upload.full_clean()
                        upload.save()
                        file_url = upload.file.url

                        # Add upload to team files
                        team_id = request.POST.get("team_id")
                        if team_id is not None:
                            team = Team.objects.get(id=team_id)
                            team.add_upload(upload)
                        
                        # Share to given username / email
                        share_to = request.POST.get("share")
                        if share_to != '':
                            try:
                                user = User.objects.get(username=share_to)
                                share_instance = SharedFiles.objects.create(
                                    shared_file=upload,
                                    shared_by=request.user
                                )
                                share_instance.shared_to.add(user)
                            except User.DoesNotExist:
                                try:
                                    user = User.objects.get(email=share_to)
                                    share_instance = SharedFiles.objects.create(
                                        shared_file=upload,
                                        shared_by=request.user
                                    )
                                    share_instance.shared_to.add(user)
                                except User.DoesNotExist:
                                    messages.add_message(request, messages.WARNING, f'File has been uploaded but not shared. Provided username or email does not exist.')


                    except ValidationError as e:
                        messages.add_message(request, messages.ERROR, e.message_dict['file'][0])
                else:
                    messages.add_message(request, messages.ERROR, f'The Amazon S3 service is not connected.')
        else:
            form = FileForm()
    if file_url:
        context['file_url'] = file_url

    uploaded_file = Upload.objects.last()
    if uploaded_file:
        simple_file_name = uploaded_file.get_file_name_without_path()
        context['simple_file_name'] = simple_file_name

    context['form'] = form
    context['shared'] = SharedFiles.objects.filter(shared_to=current_user)
    return render(request, 'upload_file.html', context)
