# test_rename_upload_view.py
import os
from audioop import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from tasks.models import Upload
from tasks.models.user import User
from tasks.tests.helpers import reverse_with_next


class RenameUploadViewTest(TestCase):
    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        os.environ['USE_S3'] = 'TRUE'
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('rename_upload', args=[1])
        self.uploaded_file = SimpleUploadedFile("file.pdf", b"content", content_type="application/pdf")
        self.upload = Upload.objects.create(file=self.uploaded_file, owner=self.user)

    def tearDown(self):
        if self.upload:
            self.upload.delete()

    def log_in(self):
        self.client.login(username='@johndoe', password='Password123')

    def test_rename_upload_view(self):
        self.client.login(username='@johndoe', password='Password123')
        new_name = "new_file_name"
        response = self.client.post(reverse('rename_upload', args=[self.upload.id]), {'new_name': new_name})

        self.assertEqual(response.status_code, 302)

        updated_upload = Upload.objects.get(id=self.upload.id)
        self.assertNotEqual(updated_upload.file.name.split('/')[-1], new_name)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "File renamed successfully.")

        updated_upload.delete()

    def test_rename_upload_view_existing_name(self):
        self.client.login(username='@johndoe', password='Password123')
        existing_name = self.upload.file.name.split('/')[-1]
        response = self.client.post(reverse('rename_upload', args=[self.upload.id]), {'new_name': existing_name})

        self.assertEqual(response.status_code, 302)

        updated_upload = Upload.objects.get(id=self.upload.id)
        self.assertEqual(updated_upload.file.name.split('/')[-1], existing_name.split('/')[-1])

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "The new name must be different from the current name.")

    def test_rename_upload_view_error(self):
        self.client.login(username='@johndoe', password='Password123')
        invalid_name = ""
        response = self.client.post(reverse('rename_upload', args=[self.upload.id]), {'new_name': invalid_name})

        self.assertEqual(response.status_code, 302)

        updated_upload = Upload.objects.get(id=self.upload.id)
        self.assertNotEqual(updated_upload.file.name.split('/')[-1], invalid_name)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn("File with this name already exists.", str(messages[0]))

    def test_get_rename_upload_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('filelist'), status_code=302, target_status_code=200)

    def test_get_rename_upload_view_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_rename_upload_view_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, {'new_name': 'new_name'})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)