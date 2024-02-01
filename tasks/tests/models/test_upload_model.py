"""Unit tests for the Upload model."""
from unittest.mock import patch, MagicMock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.models import User, Upload


class UploadModelTestCase(TestCase):
    """Unit tests for the Upload model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        """Set up the test case."""
        file_content = b'Test file content'
        self.mock_file_1 = SimpleUploadedFile('test_file_1.pdf', file_content)
        self.mock_file_2 = SimpleUploadedFile('test_file_2.pdf', file_content)
        self.mock_file_3 = SimpleUploadedFile('test_file_3.pdf', file_content)

        self.user = User.objects.get(username='@johndoe')

        self.upload_1 = Upload.objects.create(
            owner=self.user,
            file=self.mock_file_1
        )

        self.upload_2 = Upload.objects.create(
            owner=self.user,
            file=self.mock_file_2
        )

        self.upload_3 = Upload.objects.create(
            owner=self.user,
            file=self.mock_file_3
        )

    def test_uploaded_file_url(self):
        """Test the file's url of the Upload model."""
