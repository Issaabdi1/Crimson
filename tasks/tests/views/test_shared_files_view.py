"""Tests of the shared files view."""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from tasks.models import User, SharedFiles

class SharedFilesViewTestCase(TestCase):
    """Tests of the shared files view."""

    fixtures = ['tasks/tests/fixtures/default_user.json', 'tasks/tests/fixtures/other_users.json']

    def setUp(self):
        self.url = reverse('shared_file_list')
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")
        second_user = User.objects.get(username="@janedoe")
        file_content = b'Test file content'
        mock_file = SimpleUploadedFile(f'test_file.pdf', file_content)
        self.shared_file = SharedFiles.objects.create(shared_file= mock_file, shared_by = second_user, shared_to = self.user)

    def test_home_url(self):
        self.assertEqual(self.url,'/shared_file_list/')

    def test_get_shared_files(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shared_file_list.html')

    def test_shared_files_passed_in(self):
        response = self.client.get(self.url, follow=True)
        user = response.context['user']
        self.assertEqual(self.user, user) 
        shared_files = response.context['shared_files']
        self.assertIsNotNone(shared_files)
        self.assertIn(self.shared_file, shared_files)