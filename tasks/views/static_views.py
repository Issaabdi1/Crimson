"""Static views of the tasks app."""
from django.shortcuts import render
from tasks.helpers import login_prohibited

@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')