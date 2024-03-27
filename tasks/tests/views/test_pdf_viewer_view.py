"""Tests of the pdf viewer view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Upload
from django.core.files.uploadedfile import SimpleUploadedFile

class PDFViewerViewTest(TestCase):
    """Tests of the pdf viewer view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('pdf_viewer')
        self.user = User.objects.get(username='@johndoe')
        self.uploaded_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        self.upload = Upload.objects.create(file=self.uploaded_file, owner=self.user)

    def tearDown(self):
        if self.upload:
            self.upload.delete()

    def login(self, user):
        self.client.login(username=user.username, password='Password123')

    def test_pdf_viewer_url(self):
        self.assertEqual(self.url, '/pdf_viewer/')

    def test_get_viewer(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer.html')

    def test_post_valid_upload_id(self):
        self.login(self.user)
        response = self.client.post(self.url, {'upload_id': self.upload.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer.html')
        self.assertIn('upload', response.context)
        self.assertEqual(response.context['upload'], self.upload)

    def test_post_invalid_upload_id(self):
        self.login(self.user)
        response = self.client.post(self.url, {'upload_id': -1}) # Impossible upload id
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer.html')
        self.assertIn('messages', response.context)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Upload does not exist!")