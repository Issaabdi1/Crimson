"""Unit tests for the Upload model."""
from unittest.mock import patch, MagicMock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.models import User, Upload
from urllib.parse import quote
from urllib.request import urlopen


class UploadModelTestCase(TestCase):
    """Unit tests for the Upload model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        """Set up the test case."""
        file_content = b'Test file content'
        self.user = User.objects.get(username='@johndoe')
        self.mock_files = []
        self.uploads = []

        for i in range(1, 4):
            mock_file = SimpleUploadedFile(f'test_file_{i}.pdf', file_content)
            upload = Upload.objects.create(owner=self.user, file=mock_file)
            self.mock_files.append(mock_file)
            self.uploads.append(upload)

    def tearDown(self):
        for upload in self.uploads:
            upload.delete()

    def test_uploaded_file_url(self):
        """Test the file's url of the Upload model."""
        for upload in self.uploads:
            self.assertEqual(
                upload.file.url,
                f'https://mypdfbucket01.s3.amazonaws.com/media/{quote(upload.file.name)}'
            )

    def test_upload_delete(self):
        """Test that the upload delete will delete the file in the server"""
        for upload in self.uploads:
            file_url = upload.file.url
            self.assertEqual(urlopen(file_url).getcode(), 200)
            upload.delete()
            self.assertFalse(Upload.objects.filter(pk=upload.pk).exists())
            self.assertEqual(urlopen(file_url).getcode(), 404)

    def test_ordering(self):
        """Test that uploads are ordered by uploaded_at."""
        uploads = Upload.objects.all()
        self.assertEqual(list(uploads), self.uploads)