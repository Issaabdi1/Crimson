# voice_comment_views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tasks.models import Upload,VoiceComment
from django.core.exceptions import ValidationError
from django.contrib import messages


@login_required
def voice_comment_views(request, upload_id):
    context = {'user': request.user}
    upload = Upload.objects.get(id=upload_id)
    image_url = None

    if request.method == 'POST':
        audio_filec = request.FILES['audio_file']

        if settings.USE_S3:
            voicecomment = VoiceComment(soundfile= audio_filec, owner=request.user,upload=upload)
            try:
                voicecomment.full_clean()
                voicecomment.save()
                image_url = voicecomment.soundfile.url
                messages.success(request, 'Voice Comment saved successfully.')
            except ValidationError as e:
                messages.add_message(request, messages.ERROR, e.message_dict['file'][0])
        else:
            messages.add_message(request, messages.ERROR, f'The Amazon S3 service is not connected.')

    if image_url:
        context['image_url'] = image_url

    return redirect ('filelist')



