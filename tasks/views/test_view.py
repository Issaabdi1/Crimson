"""Javascript test view"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def test(request):
    """Displays the test file for the javascript tests."""
    return render(request, 'test.html')