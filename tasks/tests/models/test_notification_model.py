"""Unit tests for the Notification model."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User, Notification, SharedFiles, Upload
from datetime import datetime 

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
        self.notification = Notification.objects.create(shared_file_instance=shared_file, time_of_notification=datetime.now(), user=self.user)


    def test_valid_notification(self):
        self._assert_notification_is_valid()

    def test_shared_file_cannot_be_none(self):
        self.notification.shared_file_instance = None
        self._assert_notification_is_invalid()

    def test_user_cannot_be_none(self):
        self.notification.user = None
        self._assert_notification_is_invalid()

    def test_date_cannot_be_blank(self):
        self.notification.time_of_notification = None
        self._assert_notification_is_invalid()

    def _assert_notification_is_valid(self):
        try:
            self.notification.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_notification_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.notification.full_clean()