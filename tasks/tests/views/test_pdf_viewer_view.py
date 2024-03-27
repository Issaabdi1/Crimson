"""Tests of the pdf viewer view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Upload, PDFInfo, VoiceComment
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from tasks.tests.helpers import reverse_with_next
from tasks.views import viewer


class PDFViewerViewTest(TestCase):
    """Tests of the pdf viewer view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('pdf_viewer')
        self.user = User.objects.get(username='@johndoe')
        self.uploaded_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        self.upload = Upload.objects.create(file=self.uploaded_file, owner=self.user)
        self.pdf_info = PDFInfo.objects.create(upload=self.upload, mark_id=1, listOfSpans="[{\"index\":1,\"html\":\"Lorem Ipsum is simply dummy text <span id=\\\\\\\"}]", listOfComments="[{\"index\":1,\"html\":\"Lorem Ipsum is simply dummy text <span id=\\\\\\\"}]")
        self.mock_audio = SimpleUploadedFile('test_voice_comment_model_audio.wav', '')
        self.voice_comment = VoiceComment.objects.create(
            user=self.user,
            upload=self.upload,
            mark_id=1,
            audio=self.mock_audio,
        )

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()
        if PDFInfo.objects.all():
            PDFInfo.objects.all().delete()

    def login(self, user):
        self.client.login(username=user.username, password='Password123')

    def test_pdf_viewer_url(self):
        self.assertEqual(self.url, '/pdf_viewer/')

    def test_get_viewer(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer.html')

    def test_get_viewer_redirects_when_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_viewer_redirects_when_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, {'upload_id': self.upload.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

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

    def test_post_without_upload_id(self):
        self.login(self.user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer.html')
        self.assertIn('messages', response.context)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), f'Upload id was not specified in the form!')

    def test_post_viewer_without_mark(self):
        self.login(self.user)
        response = self.client.post(self.url, {'upload_id': self.upload.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer.html')
        self.assertIn('upload', response.context)
        self.assertIn('current_user', response.context)
        self.assertEqual(response.context['upload'], self.upload)
        self.assertEqual(response.context['current_user'], self.user)

    def test_post_viewer_with_mark(self):
        self.login(self.user)
        response = self.client.post(self.url, {'upload_id': self.upload.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer.html')
        self.assertIn('upload', response.context)
        self.assertIn('marks', response.context)
        self.assertIn('listOfSavedComments', response.context)
        self.assertIn('current_user', response.context)
        self.assertEqual(response.context['upload'], self.upload)
        self.assertEqual(response.context['current_user'], self.user)

    def test_post_viewer_without_voice_comment(self):
        self.login(self.user)
        self.voice_comment.delete()
        response = self.client.post(self.url, {'upload_id': self.upload.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer.html')
        self.assertIn('upload', response.context)
        self.assertIn('marks', response.context)
        self.assertIn('current_user', response.context)
        self.assertEqual(response.context['upload'], self.upload)
        self.assertEqual(response.context['current_user'], self.user)