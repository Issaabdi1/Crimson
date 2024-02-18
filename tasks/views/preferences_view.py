from django.shortcuts import render
from django.http import HttpResponse

def preferences_view(request):

    if request.method == 'POST':
        selected_theme = request.POST.get('themeSelection')

        if selected_theme:
            request.user.theme_preference = selected_theme
            request.user.save()
        else:
            selected_theme = request.user.theme_preference

    return render(request, 'preferences.html', {'selected_theme': selected_theme})