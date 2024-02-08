"""Tests of the navigation sidebar."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User

class SidebarTestCase(TestCase):
    """Tests of the navigation sidebar."""

    #test that when the button is clicked, go to the correct web page
    #also test that the correct button is active for each one
    
    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='@johndoe')

    def test_home_button(self):
        self.url=""
        #test that when home pressed, home page is reached, and the button is set active

    def test_my_files_button(self):
        self.url=""
        #test that when my_files pressed, my_files page is reached, and the button is set active

    def test_shared_files_button(self):
        self.url=""
        #test that when shared_files pressed, shared_files page is reached, and the button is set active
