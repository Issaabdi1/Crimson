from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def preferences_view(request):
    selected_theme = request.user.theme_preference 

    if request.method == 'POST':
        new_selected_theme = request.POST.get('themeSelection')
        if new_selected_theme:
            request.user.theme_preference = new_selected_theme
            request.user.save()
            selected_theme = new_selected_theme  

    return render(request, 'preferences.html', {'selected_theme': selected_theme})
