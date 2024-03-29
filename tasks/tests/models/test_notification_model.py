"""Unit tests for the Notification model."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User, Notification, SharedFiles, Upload
from django.utils import timezone

class NotificationModelTestCase(TestCase):
    """Unit tests for the Notification model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        """Creates a notification from sharing a file from the second user to the first"""
        self.user = User.objects.get(username='@johndoe')
        second_user = User.objects.get(username="@janedoe")
        file_content = b'Test file content'
        mock_file = SimpleUploadedFile(f'test_file.pdf', file_content)
        self.upload = Upload.objects.create(owner=self.user, file=mock_file)
        shared_file = SharedFiles.objects.create(shared_file= self.upload, shared_by = second_user)
        shared_file.shared_to.add(self.user)
        self.notification = Notification.objects.create(upload=self.upload, shared_file_instance=shared_file, time_of_notification=timezone.now(), user=self.user, notification_message="Hello")

    def tearDown(self):
        self.upload.delete()

    def test_valid_notification(self):
        self._assert_notification_is_valid()

    def test_upload_cannot_be_none(self):
        self.notification.upload = None
        self._assert_notification_is_invalid()

    def test_shared_file_can_be_none(self):
        self.notification.shared_file_instance = None
        self._assert_notification_is_valid()

    def test_user_cannot_be_none(self):
        self.notification.user = None
        self._assert_notification_is_invalid()

    def test_date_cannot_be_blank(self):
        self.notification.time_of_notification = None
        self._assert_notification_is_invalid()
    
    def test_message_cannot_be_blank(self):
        self.notification.notification_message = ""
        self._assert_notification_is_invalid()

    def _assert_notification_is_valid(self):
        try:
            self.notification.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_notification_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.notification.full_clean()
    
    def tearDown(self):
        self.upload.delete()