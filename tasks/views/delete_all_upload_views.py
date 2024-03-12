from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from tasks.models import Upload


@login_required
def delete_all_upload_views(request):
    if request.method == 'POST':
        upload = Upload.objects.all()
        upload.delete()
        return HttpResponseRedirect(reverse('filelist'))
    else:
        return HttpResponseRedirect(reverse('filelist'))
