# test_delete_upload_view.py
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
from tasks.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
import os

from tasks.tests.helpers import reverse_with_next


class DeleteUploadTestCase(TestCase):
    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        os.environ['USE_S3'] = 'TRUE'
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('delete_upload', args=[1])
        self.uploaded_file = SimpleUploadedFile("file.pdf", b"content", content_type="application/pdf")

    def log_in(self):
        self.client.login(username='@johndoe', password='Password123')

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()

    def test_get_delete_upload(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('filelist')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_delete_upload_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_delete_upload_should_delete_upload(self):
        self.log_in()
        upload = Upload.objects.create(owner=self.user, file=self.uploaded_file)
        before_count = Upload.objects.count()
        response = self.client.post(self.url, {})
        after_count = Upload.objects.count()
        self.assertEqual(before_count - 1, after_count)
        self.assertEqual(response.status_code, 302)

    def test_post_delete_upload_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, {})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_upload_pdf(self):
        self.log_in()
        pdf_content = b"content"
        pdf = SimpleUploadedFile("file.pdf", pdf_content, content_type="application/pdf")
        response = self.client.post(reverse('filelist'), {'pdf': pdf}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_upload_and_delete_pdf(self):
        pdf_content = b"content"
        pdf = SimpleUploadedFile("file.pdf", pdf_content, content_type="application/pdf")
        response = self.client.post(reverse('filelist'), {'pdf': pdf}, follow=True)
        self.assertEqual(response.status_code, 200)

        uploaded_file = Upload.objects.filter(id=1)
        self.assertIsNotNone(uploaded_file)

        response_filelist = self.client.get(self.url, follow=True)
        self.assertEqual(response_filelist.status_code, 200)

        response_delete = self.client.post(reverse('delete_upload', args=[1]), follow=True)
        self.assertEqual(response_delete.status_code, 200)

        response = HttpResponseRedirect(reverse('filelist'))
        self.assertEqual(response.status_code, 302)

        self.assertNotContains(response_delete, 'file.pdf')

    def test_delete_upload_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('delete_upload', args=[1]))
        self.assertRedirects(response, reverse('log_in') + f'?next={reverse("delete_upload", args=[1])}')

    def test_delete_upload_authenticated(self):
        self.client.login()
        response = self.client.post(reverse('delete_upload', args=[1]))
        self.assertRedirects(response, reverse('log_in') + f'?next={reverse("delete_upload", args=[1])}')
