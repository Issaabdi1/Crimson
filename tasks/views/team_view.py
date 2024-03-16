from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from tasks.forms import CreateTeamForm, AddUserToTeamForm, FileForm
from tasks.models import User, Team


@login_required
def list_team_view(request):
    current_user = request.user
    team_joined = current_user.team_set.all()
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            team.members.add(current_user)
            team.save()
            return redirect('team_list')
    else:
        form = CreateTeamForm()
    context = {'user': current_user,
               'team_joined': team_joined,
               'form': form,}
    return render(request, 'list_team.html',  context=context)


@login_required
def team_detail_view(request, team_id):
    current_user = request.user
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
    else:
        form = AddUserToTeamForm()

    upload_form =  FileForm()
    context = {'user': current_user,
               'team': team,
               'members': members,
               'shared_uploads': shared_uploads,
               'form': form,
               'upload_form': upload_form}
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