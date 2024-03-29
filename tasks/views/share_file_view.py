"""Share file related views"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from tasks.models import User, Upload, SharedFiles, Notification
from django.utils import timezone


@login_required
def shared_file_list(request):
    """Display the current user's shared files."""
    current_user = request.user
    shared_files = SharedFiles.objects.filter(shared_to=current_user).order_by('shared_date')

    page_number = request.GET.get('page', 1)
    per_page = 6
    paginator = Paginator(shared_files, per_page)
    page_obj = paginator.get_page(page_number)

    context = {'shared_files': page_obj.object_list,
               'user': current_user,
               "paginator": paginator,
               "current_page": paginator.page(page_number),
               "last_three_page": paginator.num_pages - 2,
               "last_few_pages": paginator.num_pages - 4,
               "next_few_page": int(page_number) + 3,
               }
    return render(request, 'shared_file_list.html', context)


@login_required
def share_file(request):
    """Display view handling shared files"""
    user = request.user
    all_users = User.objects.exclude(username=user.username)
    uploads = Upload.objects.filter(owner=user)
    if Upload.objects.filter(owner=user).count() == 0:
        messages.warning(request, 'Please upload a file before sharing.')
    if request.method == 'POST':
        file_id = request.POST.get('file-id')
        user_ids = request.POST.get('user-ids')
        if file_id is not None and user_ids:
            shared_file = Upload.objects.get(id=file_id)
            user_list = user_ids.split(',')
            for user_id in user_list:
                shared_user = User.objects.get(id=user_id)
                entry, created = SharedFiles.objects.get_or_create(
                    shared_file=shared_file,
                    shared_by=user,
                )
                if entry.shared_to.contains(shared_user):
                    messages.error(request, f'User {shared_user.username} has already been shared this file.')
                else:
                    # Create a new notification if the file has been newly shared
                    Notification.objects.create(
                        upload=entry.shared_file,
                        shared_file_instance=entry,
                        user=shared_user,
                        time_of_notification=timezone.now(),
                        notification_message=f'{request.user} shared a file with you'
                    )
                entry.shared_to.add(shared_user)
                entry.save()
        elif file_id is None:
            messages.error(request, 'Please select a file to share.')
        elif file_id is not None and len(user_ids)<=0:
            messages.error(request, 'Please select a user to share this file to.')

    context = {
        'uploads': uploads,
        'all_users': all_users,
    }
    return render(request, 'share_file.html', context)