from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from tasks.models import Upload


@login_required
def delete_upload(request, upload_id):
    if request.method == 'POST':
        upload = get_object_or_404(Upload, pk=upload_id, owner=request.user)
        upload.file.delete()
        upload.delete()
        return HttpResponseRedirect(reverse('filelist'))
    else:
        return HttpResponseRedirect(reverse('filelist'))


@login_required
def delete_all_upload_views(request):
    if request.method == 'POST':
        upload = Upload.objects.filter(owner=request.user)
        upload.delete()
        return HttpResponseRedirect(reverse('filelist'))
    else:
        return HttpResponseRedirect(reverse('filelist'))
