"""Tests of the file list view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Upload
from django.core.files.uploadedfile import SimpleUploadedFile

class PDFViewerViewTest(TestCase):
    """Tests of the file list view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('filelist')
        self.user = User.objects.get(username='@johndoe')
        self.uploaded_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        self.upload = Upload.objects.create(file=self.uploaded_file, owner=self.user)
        self.other_file = SimpleUploadedFile("test2.pdf", b"file_content", content_type="application/pdf")
        self.upload2 = Upload.objects.create(file=self.other_file, owner=self.user)

    def tearDown(self):
        if self.upload:
            self.upload.delete()
        if self.upload2:
            self.upload2.delete()
    
    def login(self, user):
        self.client.login(username=user.username, password='Password123')
    
    def test_filelist_url(self):
        self.assertEqual(self.url, '/filelist/')

    def test_get_filelist(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filelist.html')
    
    def test_post_filelist(self):
        self.login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filelist.html')

    def test_filelist_shows_all_user_uploads(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertIn('uploads', response.context)
        self.assertIn(self.upload, response.context['uploads'])
        self.assertIn(self.upload2, response.context['uploads'])

