from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def create_team_view(request):
    return render(request, 'create_team.html')


@login_required
def list_team_view(request):
    return render(request, 'list_team.html')


@login_required
def list_team_file_view(request):
    return render(request, 'list_team_file.html')