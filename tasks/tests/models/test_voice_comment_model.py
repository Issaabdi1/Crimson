"""Unit tests for the Voice Comment model"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User, Upload, VoiceComment
from tasks.models.voice_comment import user_directory_path
from urllib.parse import quote


class VoiceCommentModelTestCase(TestCase):

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        mock_file = SimpleUploadedFile('test_voice_comment_model_file.pdf', '')
        self.mock_audio = SimpleUploadedFile('test_voice_comment_model_audio.wav', '')
        self.upload = Upload.objects.create(owner=self.user, file=mock_file)
        self.voice_comment = VoiceComment.objects.create(
            user=self.user,
            upload=self.upload,
            mark_id=1,
            audio=self.mock_audio,
        )

    def tearDown(self):
        default_storage.delete(self.voice_comment.audio.name)
        self.voice_comment.delete()
        self.upload.delete()
        super().tearDown()
    
    def test_valid_voice_comment(self):
        self._assert_voice_comment_is_valid()
    
    def test_user_cannot_be_blank(self):
        self.voice_comment.user = None
        self._assert_voice_comment_is_invalid()
        self.voice_comment.user = self.user

    def test_upload_cannot_be_blank(self):
        self.voice_comment.upload = None
        self._assert_voice_comment_is_invalid()
        self.voice_comment.upload = self.upload
    
    def test_audio_cannot_be_blank(self):
        audio_name = self.voice_comment.audio.name
        self.voice_comment.audio = None
        self._assert_voice_comment_is_invalid()
        self.voice_comment.audio = audio_name

    def test_audio_file_url(self):
        self.assertEqual(
            self.voice_comment.audio.url,
            f'https://mypdfbucket01.s3.amazonaws.com/media/{quote(self.voice_comment.audio.name)}'
        )
    
    def test_audio_names_do_not_match(self):
        filenames = [user_directory_path(self.voice_comment, self.mock_audio.name) for _ in range(100)]
        self.assertEqual(len(set(filenames)), len(filenames))

    def _assert_voice_comment_is_valid(self):
        try:
            self.voice_comment.full_clean()
        except ValidationError:
            self.fail('Test voice comment should be valid')

    def _assert_voice_comment_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.voice_comment.full_clean()
