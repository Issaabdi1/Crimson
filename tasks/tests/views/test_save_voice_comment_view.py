"""Unit tests for saving voice comments"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.test import TestCase
from django.urls import reverse
from tasks.models import *
import json, base64


class SaveVoiceCommentViewTestCase(TestCase):

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('save_voice_comments')
        self.user = User.objects.get(username='@johndoe')
        mock_file = SimpleUploadedFile('test_VC_file.pdf', '')

        self.mock_audio = SimpleUploadedFile('test_audio.wav', b'test content 1')
        self.mock_audio2 = SimpleUploadedFile('test_audio2.wav', b'test content 2')
        self.mock_audio3 = SimpleUploadedFile('test_audio3.wav', b'test content 3')

        # Encode files using base64 since view decodes files before saving
        # This is because JSON requires audio to be converted to binary data in order to be sent from front-end
        self.encoded_audio = base64.b64encode(self.mock_audio.read()).decode()
        self.encoded_audio2 = base64.b64encode(self.mock_audio2.read()).decode()
        self.encoded_audio3 = base64.b64encode(self.mock_audio3.read()).decode()

        # Add base transcripts for the first two audios
        self.transcript = "test transcript 1"
        self.transcript2 = "test transcript 2"

        self.upload = Upload.objects.create(owner=self.user, file=mock_file)
        self.voice_comment_list = {
            1: [
                {"blob": self.encoded_audio, "transcript": self.transcript}, 
                {"blob": self.encoded_audio2, "transcript": self.transcript2}
            ],
            2: [
                {"blob": self.encoded_audio3}
            ]
        }
        self.successful_save = False

    def tearDown(self):
        if self.successful_save:
            vcs = VoiceComment.objects.filter(upload=self.upload)
            for vc in vcs:
                default_storage.delete(vc.audio.name)
                vc.delete()
        if Upload.objects.all():
            Upload.objects.all().delete()
        if VoiceComment.objects.all():
            VoiceComment.objects.all().delete()
        super().tearDown()

    def test_save_voice_comments_url(self):
        self.assertEqual(self.url, '/save_voice_comments/')

    def test_GET_request_does_not_save(self):
        before_count = VoiceComment.objects.count()
        response = self.client.get(self.url)
        after_count = VoiceComment.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)

    def test_POST_request_with_missing_data_returns_BAD_REQUEST_error(self):
        before_count = VoiceComment.objects.count()
        response = self.client.post(self.url, {'upload_id': self.upload.id})
        after_count = VoiceComment.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 400)

    def test_POST_request_with_no_voice_comments_returns_NOT_FOUND_error(self):
        before_count = VoiceComment.objects.count()
        response = self.client.post(self.url, {'upload_id': self.upload.id, 'voice-comment-list': '[]'})
        after_count = VoiceComment.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 404)

    def test_successful_save(self):
        voice_comment_str = json.dumps(self.voice_comment_list)
        self.client.login(username=self.user.username, password='Password123')
        before_count = VoiceComment.objects.count()
        response = self.client.post(self.url, {
            'upload_id': self.upload.id, 
            'voice-comment-list': voice_comment_str,
        })
        after_count = VoiceComment.objects.count()
        self.assertEqual(before_count + 3, after_count)

        # Check that audio on the second mark has no transcript
        audio_with_no_transcript = VoiceComment.objects.get(mark_id=2)
        self.assertFalse(audio_with_no_transcript.transcript) # None and '' evaluate to False

        self.assertEqual(response.status_code, 200)
        self.successful_save = True

    def test_post_mark_as_resolved(self):
        url = reverse('mark_as_resolved')
        self.client.login(username=self.user.username, password='Password123')
        self.mock_audio = SimpleUploadedFile('test_voice_comment_model_audio.wav', '')
        other_voice_comment = VoiceComment.objects.create(
            user=self.user,
            upload=self.upload,
            mark_id=1,
            audio=self.mock_audio,
        )
        post_data = {
            'audio_url': other_voice_comment.audio.url
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        other_voice_comment.refresh_from_db()
        self.assertTrue(other_voice_comment.is_resolved)

    def test_post_mark_as_resolved_with_wrong_url(self):
        url = reverse('mark_as_resolved')
        self.client.login(username=self.user.username, password='Password123')
        self.mock_audio = SimpleUploadedFile('test_voice_comment_model_audio.wav', '')
        other_voice_comment = VoiceComment.objects.create(
            user=self.user,
            upload=self.upload,
            mark_id=1,
            audio=self.mock_audio,
        )
        post_data = {
            'audio_url': other_voice_comment.audio.url + '111'
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        other_voice_comment.refresh_from_db()
        self.assertFalse(other_voice_comment.is_resolved)

    def test_get_mark_as_resolved(self):
        url = reverse('mark_as_resolved')
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '{}')