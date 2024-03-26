from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from tasks.forms import CreateTeamForm, AddUserToTeamForm, FileForm, JoinTeamForm
from tasks.models import User, Team, Upload, Notification
from django.utils import timezone

@login_required
def list_team_view(request):
    current_user = request.user
    team_joined = current_user.team_set.all()
    create_form = CreateTeamForm()
    join_form = JoinTeamForm()
    if request.method == 'POST':
        if 'create_group' in request.POST:
            create_form = CreateTeamForm(request.POST)
            if create_form.is_valid():
                team = create_form.save()
                team.members.add(current_user)
                team.save()
                return redirect('team_list')
        elif 'join_group' in request.POST:
            join_form = JoinTeamForm(request.POST)
            if join_form.is_valid():
                team = Team.objects.all().filter(invitation_code=join_form.cleaned_data['invitation_code'])[0]
                team.members.add(current_user)
                team.save()
                return redirect('team_list')

    context = {'user': current_user,
               'team_joined': team_joined,
               'create_form': create_form,
               'join_form': join_form}
    return render(request, 'list_team.html',  context=context)


@login_required
def team_detail_view(request, team_id):
    current_user = request.user
    my_uploads = Upload.objects.filter(owner=current_user)
    try:
        team = current_user.team_set.get(id=team_id)
    except Team.DoesNotExist:
        messages.add_message(request, messages.ERROR, f'You are not allowed to access this team')
        return redirect('team_list')
    members = team.members.all()
    shared_uploads = team.shared_uploads.all()
    if request.method == 'POST':
        form = AddUserToTeamForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user_to_add = User.objects.get(username=username)
                team.members.add(user_to_add)
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, f'The user invited is not exist, please try another one.')
        if 'share-file' in request.POST:
            file_id = request.POST.get('file-id')
            if file_id is not None:
                shared_file = Upload.objects.get(id=file_id)
                if team.shared_uploads.contains(shared_file):
                    messages.add_message(request, messages.ERROR, f'This file has already been shared.')
                else:
                    team.shared_uploads.add(shared_file)
                    team.save()
                    for member in members:
                        if member!=current_user:
                            Notification.objects.create(
                                upload=shared_file,
                                shared_file_instance=None,
                                user=member,
                                time_of_notification=timezone.now(),
                                notification_message=f'{request.user} added a file to team {team.name}'
                            )
            else:
                messages.add_message(request, messages.ERROR, f'Please select a file to share.')
    else:
        form = AddUserToTeamForm()

    page_number = request.GET.get('page', 1)
    per_page = 4
    paginator = Paginator(shared_uploads, per_page)
    page_obj = paginator.get_page(page_number)

    upload_form =  FileForm()
    context = {'user': current_user,
               'team': team,
               'members': members,
               'shared_uploads': page_obj.object_list,
               'form': form,
               'upload_form': upload_form,
               'uploads': my_uploads,
               "paginator": paginator,
               "current_page": paginator.page(page_number),
               "last_three_page": paginator.num_pages - 2,
               "last_few_pages": paginator.num_pages - 4,
               "next_few_page": int(page_number) + 3,
               }
    return render(request, 'team_detail.html', context=context)


@login_required
def leave_team_view(request, team_id):
    current_user = request.user
    try:
        team = current_user.team_set.get(id=team_id)
    except Team.DoesNotExist:
        messages.add_message(request, messages.ERROR, f'You are not allowed to access this team')
        return redirect('team_list')
    team.members.remove(current_user)
    if team.members.count() > 0:
        team.save()
    else:
        team.delete()
    return redirect('team_list')