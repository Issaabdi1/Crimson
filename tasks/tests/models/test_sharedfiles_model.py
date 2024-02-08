from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.models import User, Upload, SharedFiles
from django.utils import timezone
from datetime import timedelta

class SharedFilesModelTestCase(TestCase):

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')
        self.test_file = SimpleUploadedFile(
            'test_file.pdf',
            b'Test file content',
            content_type='text/plain'
        )
        self.upload = Upload.objects.create(
            file=self.test_file, 
            owner=self.user
        )
        self.share = SharedFiles.objects.create(
            shared_file=self.upload, 
            shared_by=self.user
        )
        self.share.shared_to.add(self.second_user)

    def test_valid_share(self):
        self._assert_share_is_valid()
    
    def test_file_must_not_be_blank(self):
        self.share.shared_file = None
        self._assert_share_is_invalid()
    
    def test_shared_by_must_not_be_blank(self):
        self.share.shared_by = None
        self._assert_share_is_invalid()

    def test_shared_to_can_be_blank(self):
        self.share.shared_to.set([None])
        self._assert_share_is_valid()

    def test_date_saved_correctly(self):
        second_share = SharedFiles.objects.create(
            shared_file=self.upload,
            shared_by=self.user
        )
        self.assertAlmostEqual(second_share.date, timezone.now(), delta=timedelta(seconds=1))

    def _assert_share_is_valid(self):
        try:
            self.share.full_clean()
        except (ValidationError):
            self.fail('Test file should be valid')

    def _assert_share_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.share.full_clean()