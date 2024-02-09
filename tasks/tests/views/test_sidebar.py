"""Tests of the navigation sidebar."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User

class SidebarTestCase(TestCase):
    """Tests of the navigation sidebar."""
    
    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")

    def test_home_button(self):
        """Tests when on the dashboard that the home button is highlighted"""
        dashboard_url = reverse('dashboard')
        response= self.client.get(dashboard_url)
        self.assertContains(response, f'<a class="nav-link active text-center" aria-current="page" href="{dashboard_url}">Home</a>', status_code=200 )
        self.assertTemplateUsed( response, 'dashboard.html' )

    def test_my_files_button(self):
        """Tests when on the my files page that the my files button is highlighted"""
        filelist_url = reverse('filelist')
        response= self.client.get(filelist_url)
        self.assertContains(response, f'<a class="nav-link active text-center" aria-current="page" href="{filelist_url}">My Files</a>', status_code=200 )
        self.assertTemplateUsed( response, 'filelist.html' )

    def test_shared_files_button(self):
        """Tests when on the shared files page that the shared to me button is highlighted"""
        shared_file_list_url = reverse('shared_file_list')
        response= self.client.get(shared_file_list_url)
        self.assertContains(response, f'<a class="nav-link active text-center" aria-current="page" href="{shared_file_list_url}">Shared To Me</a>', status_code=200 )
        self.assertTemplateUsed( response, 'shared_file_list.html' )