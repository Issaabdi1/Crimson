"""Javascript test view"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import Upload, User
from django.contrib.auth.decorators import user_passes_test


@login_required
def test(request):
    """Displays the test file for the javascript tests."""
    return render(request, 'test.html')


"""Before testing, make sure run the command 'create_debug_superuser' 
to create the superuser @admin with two default test files """


def superuser_required(user):
    return user.is_superuser


@login_required()
@user_passes_test(superuser_required)
def test_viewer_1(request):
    """Open the pdf viewer with test files 1 (main) for the selenium tests"""
    admin = User.objects.get(username='@admin')
    upload = Upload.objects.filter(owner=admin)[0]
    context = {'upload': upload}
    return render(request, 'test_viewer.html', context)


@login_required()
@user_passes_test(superuser_required)
def test_viewer_2(request):
    """Open the pdf viewer with test files 2 (with outline) for the selenium tests"""
    admin = User.objects.get(username='@admin')
    upload = Upload.objects.filter(owner=admin)[1]
    context = {'upload': upload}
    return render(request, 'test_viewer.html', context)
