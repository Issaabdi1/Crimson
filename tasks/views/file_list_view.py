"""file list view"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import User, Upload
from django.utils import timezone
from django.core.paginator import Paginator


@login_required
def filelist(request):
    """Display the current user's uploaded files."""

    current_user = request.user
    uploads = Upload.objects.filter(owner=current_user)
    all_users = User.objects.exclude(username=current_user.username)

    page_number = request.GET.get('page', 1)
    per_page = 6
    paginator = Paginator(uploads, per_page)
    page_obj = paginator.get_page(page_number)

    context = {'uploads': page_obj.object_list,
               'user': current_user,
               "all_users": all_users,
               "paginator": paginator,
               "current_page": paginator.page(page_number),
               "last_three_page": paginator.num_pages - 2,
               "last_few_pages": paginator.num_pages - 4,
               "next_few_page": int(page_number)+3,
    }

    for upload in page_obj.object_list:
        time_difference = timezone.now() - upload.uploaded_at
        if time_difference.days > 0:
            upload.upload_time_difference = f"{time_difference.days} days ago"
        elif time_difference.seconds < 60:
            upload.upload_time_difference = "just now"
        elif time_difference.seconds < 3600:
            minutes = time_difference.seconds // 60
            upload.upload_time_difference = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            hours = time_difference.seconds // 3600
            upload.upload_time_difference = f"{hours} hour{'s' if hours > 1 else ''} ago"

    response = render(request, 'filelist.html', context)
    response['Refresh'] = '3600'
    return render(request, 'filelist.html', context)


