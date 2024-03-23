"""Tests for the dashboard view."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Upload
from tasks.tests.helpers import reverse_with_next
import json


class DashboardViewTest(TestCase):
    """Test suite for the dashboard view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('dashboard')
        self.upload = Upload.objects.create(owner=self.user, file=SimpleUploadedFile("test.pdf", b"file_content"))
        self.other_upload = Upload.objects.create(owner=self.user,
                                                  file=SimpleUploadedFile("test2.pdf", b"file_content2"))

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()

    def test_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard/')

    def test_get_dashboard(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_get_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, {})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_download_single_view(self):
        self.login(self.user)
        response = self.client.get(reverse('download_single', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="{self.upload.file.name}"')
        self.assertEqual(response.content, b"file_content")

    def test_download_single_view_with_invalid_upload_id(self):
        self.login(self.user)
        response = self.client.get(reverse('download_single', args=[1000]))
        self.assertEqual(response.status_code, 404)

    def test_download_single_view_unauthenticated_user(self):
        url = reverse('download_single', args=[1])
        redirect_url = reverse_with_next('log_in', url)
        response = self.client.get(url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_download_multiple_view(self):
        self.login(self.user)
        data = {'upload_ids': [self.upload.id, self.other_upload.id]}
        response = self.client.post(reverse('download_multiple'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="uploads.zip"')
        self.assertTrue(len(response.content) > 0)

    def test_download_multiple_view_invalid_method(self):
        self.login(self.user)
        response = self.client.get(reverse('download_multiple'))
        self.assertEqual(response.status_code, 405)

    def test_download_multiple_view_no_upload_ids(self):
        self.login(self.user)
        data = {}
        response = self.client.post(reverse('download_multiple'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Bad request

    def test_download_multiple_view_unauthenticated_user(self):
        url = reverse('download_multiple')
        redirect_url = reverse_with_next('log_in', url)
        data = {'upload_ids': [self.upload.id, self.other_upload.id]}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_delete_selected_uploads_view(self):
        self.login(self.user)
        before_count = Upload.objects.count()
        data = {'upload_ids': [self.upload.id, self.other_upload.id]}
        response = self.client.post(reverse('delete_selected_uploads'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success'})
        self.assertFalse(Upload.objects.filter(id__in=[self.upload.id, self.other_upload.id]).exists())
        self.assertEqual(before_count, Upload.objects.count() + 2)

    def test_delete_selected_uploads_view_invalid_method(self):
        self.login(self.user)
        response = self.client.get(reverse('delete_selected_uploads'))
        self.assertEqual(response.status_code, 405)

    def test_delete_selected_uploads_view_no_upload_ids(self):
        self.login(self.user)
        data = {}
        before_count = Upload.objects.count()
        response = self.client.post(reverse('delete_selected_uploads'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)  # No error if no upload_ids provided
        self.assertEqual(before_count, Upload.objects.count())

    def test_delete_selected_uploads_view_unauthenticated_user(self):
        url = reverse('delete_selected_uploads')
        redirect_url = reverse_with_next('log_in', url)
        data = {'upload_ids': [self.upload.id, self.other_upload.id]}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def login(self, user):
        self.client.login(username=user.username, password='Password123')
