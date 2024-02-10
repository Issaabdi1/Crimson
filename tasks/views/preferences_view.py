from django.shortcuts import render, redirect

def preferences_view(request):
    if request.method == 'POST':
        # Get the dark mode preference from the form submission
        dark_mode_preference = 'on' if 'dark_mode' in request.POST else 'off'
        # Save the preference to the session
        request.session['dark_mode'] = dark_mode_preference
        # Redirect back to the preferences page to reflect changes
        return redirect('preferences')  # Matching the name in the URL patterns

    # Retrieve the user's current dark mode preference from the session
    dark_mode_preference = request.session.get('dark_mode', 'off')  # Default to 'off'

    context = {
        'dark_mode_preference': dark_mode_preference,
    }
    return render(request, 'preferences.html', context)
