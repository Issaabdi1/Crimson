"""Unit tests for the Delete all upload view."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User, Upload
from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import HTTPError
from tasks.tests.helpers import reverse_with_next

from django.urls import reverse


class DeleteAllUploadsViewTestCase(TestCase):
    """Unit tests for the Upload model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        """Set up the test case."""
        file_content = b'Test file content'
        self.user = User.objects.get(username='@johndoe')
        self.mock_files = []
        self.uploads = []
        self.url = reverse('delete_all_upload_views')

        for i in range(1, 4):
            mock_file = SimpleUploadedFile(f'test_upload_model_file_{i}.pdf', file_content)
            upload = Upload.objects.create(owner=self.user, file=mock_file)
            self.mock_files.append(mock_file)
            self.uploads.append(upload)

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()

    def test_password_url(self):
        self.assertEqual(self.url, '/delete_all_upload/')

    def test_get_delete_all_upload_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('filelist')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_delete_all_upload_view_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_delete_all_upload_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, {})
        redirect_url = reverse('filelist')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(Upload.objects.count(), 0)

    def test_post_delete_all_upload_view_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, {})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)