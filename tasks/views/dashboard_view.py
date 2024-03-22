"""Main dashboard view"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import Upload, User
from django.core.paginator import Paginator


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
