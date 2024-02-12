from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tasks.forms import CreateTeamForm


@login_required
def create_team_view(request):
    current_user = request.user
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
               'form': form}
    return render(request, 'create_team.html', context=context)


@login_required
def list_team_view(request):
    current_user = request.user
    team_joined = current_user.team_set.all()
    context = {'user': current_user,
               'team_joined': team_joined}
    return render(request, 'list_team.html',  context=context)


@login_required
def list_team_file_view(request):
    return render(request, 'list_team_file.html')