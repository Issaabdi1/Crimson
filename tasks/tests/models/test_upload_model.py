"""Unit tests for the Upload model."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User, Upload
from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import HTTPError


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
            mock_file = SimpleUploadedFile(f'test_upload_model_file_{i}.pdf', file_content)
            upload = Upload.objects.create(owner=self.user, file=mock_file)
            self.mock_files.append(mock_file)
            self.uploads.append(upload)

    def tearDown(self):
        if self.uploads:
            for upload in self.uploads:
                upload.delete()

    def test_valid_upload(self):
        """Test that the uploads are valid."""
        for upload in self.uploads:
            self._assert_upload_is_valid(upload)

    def test_upload_owner_cannot_be_null(self):
        """Test that the owner cannot be null."""
        upload = Upload(file=self.mock_files[0])
        self._assert_upload_is_invalid(upload)

    def test_upload_file_must_not_be_extension_other_than_pdf(self):
        """Test that the file cannot be other extension."""
        upload_txt = Upload(owner=self.user,
                            file=SimpleUploadedFile('test_upload_model_file.txt', b'Test file content'))
        upload_java = Upload(owner=self.user,
                             file=SimpleUploadedFile('test_upload_model_file.java', b'Test file content'))
        upload_python = Upload(owner=self.user,
                               file=SimpleUploadedFile('test_upload_model_file.py', b'Test file content'))
        self._assert_upload_is_invalid(upload_txt)
        self._assert_upload_is_invalid(upload_java)
        self._assert_upload_is_invalid(upload_python)

    def test_uploaded_file_url(self):
        """Test the file's url of the Upload model."""
        for upload in self.uploads:
            self.assertEqual(
                upload.file.url,
                f'https://mypdfbucket01.s3.amazonaws.com/media/{quote(upload.file.name)}'
            )

    def test_uploaded_file_name(self):
        """Test the file's name of the Upload model."""
        for i in range(0, 3):
            self.assertEqual(self.uploads[i].file.name, f'user_@johndoe/{self.mock_files[i].name}')

    def test_upload_delete(self):
        """Test that the upload delete will delete the file in the server"""
        self.assertEqual(Upload.objects.count(), 3)
        for upload in self.uploads:
            file_url = upload.file.url
            self.assertEqual(urlopen(file_url).getcode(), 200)
            upload.delete()
            self.assertFalse(Upload.objects.filter(pk=upload.pk).exists())
            with self.assertRaises(HTTPError):
                self.assertEqual(urlopen(file_url).getcode(), 403)
        self.assertEqual(Upload.objects.count(), 0)
        self.uploads.clear()

    def test_ordering(self):
        """Test that uploads are ordered by uploaded_at."""
        uploads = Upload.objects.all()
        self.assertEqual(list(uploads), self.uploads)

    def _assert_upload_is_valid(self, upload):
        try:
            upload.full_clean()
        except ValidationError:
            self.fail('Test user should be valid')

    def _assert_upload_is_invalid(self, upload):
        with self.assertRaises(ValidationError):
            upload.full_clean()
