from django.shortcuts import render
from django.http import HttpResponse

def preferences_view(request):

    if request.method == 'POST':
        selected_theme = request.POST.get('themeSelection', 'default-mode')
        request.user.theme_preference = selected_theme
        request.user.save()
        print("selected theme : ")
        print(selected_theme)  # This should print the selected theme

    # If GET or after POST, use user's stored theme preference
    selected_theme = request.user.theme_preference
    return render(request, 'preferences.html', {'selected_theme': selected_theme})