"""Unit tests for deleting voice comments"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.test import TestCase
from django.urls import reverse
from tasks.models import *


class DeleteVoiceCommentViewTestCase(TestCase):

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('delete_voice_comment')
        self.user = User.objects.get(username='@johndoe')
        mock_file = SimpleUploadedFile('test_VC_file.pdf', '')
        self.mock_audio = SimpleUploadedFile('test_audio.wav', '')
        self.upload = Upload.objects.create(owner=self.user, file=mock_file)
        self.voice_comment = VoiceComment.objects.create(
            user=self.user,
            upload=self.upload,
            mark_id=1,
            audio=self.mock_audio,
        )

    def tearDown(self):
        if self.voice_comment:
            default_storage.delete(self.voice_comment.audio.name)
            self.voice_comment.delete()
        if self.upload:
            self.upload.delete()
        super().tearDown()

    def test_delete_voice_comment_url(self):
        self.assertEqual(self.url, '/delete_voice_comment/')

    def test_GET_request_does_not_delete(self):
        before_count = VoiceComment.objects.count()
        response = self.client.get(self.url)
        after_count = VoiceComment.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)

    def test_POST_request_with_no_audio_URL_does_not_delete(self):
        before_count = VoiceComment.objects.count()
        response = self.client.post(self.url)
        after_count = VoiceComment.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)

    def test_invalid_audio_URL_does_not_delete(self):
        before_count = VoiceComment.objects.count()
        response = self.client.post(self.url, {'audio-url': 'INVALID_URL'})
        after_count = VoiceComment.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 404)

    def test_successful_delete(self):
        before_count = VoiceComment.objects.count()
        response = self.client.post(self.url, {'audio-url': self.voice_comment.audio.url})
        after_count = VoiceComment.objects.count()
        self.assertEqual(before_count, after_count + 1)
        self.assertEqual(response.status_code, 200)