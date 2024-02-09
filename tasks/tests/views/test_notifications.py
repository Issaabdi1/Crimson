"""Tests of the Notifications side bar."""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from tasks.models import User, Notification, SharedFiles, Upload
from datetime import datetime

class NotificationsTestCase(TestCase):
    """Tests of the Notifications side bar."""
    
    fixtures = ['tasks/tests/fixtures/default_user.json', 'tasks/tests/fixtures/other_users.json']

    def setUp(self):
        """Creates two notifications to begin with"""
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")
        self.second_user = User.objects.get(username="@janedoe")
        file_content = b'Test file content'
        mock_file = SimpleUploadedFile(f'test_file.pdf', file_content)
        self.upload = Upload.objects.create(owner=self.user, file=mock_file)
        shared_file = SharedFiles.objects.create(shared_file= self.upload, shared_by = self.second_user)
        shared_file.shared_to.add(self.user)
        self.notification = Notification.objects.create(shared_file_instance=shared_file, time_of_notification=datetime.now(), user=self.user)
        self.notification2 = Notification.objects.create(shared_file_instance=shared_file, time_of_notification=datetime.now(), user=self.user)


    def test_notifications_passed_in(self):
        """Test that the correct notifications list is passed into the template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        notifications = response.context['notifications']
        self.assertIn(self.notification, notifications)
        self.assertIn(self.notification2, notifications)


    def test_notification_created_when_file_shared(self):
        """Shares a file, and tests if a notification is created"""
        share_files_url = reverse('share_file')
        data = {'file-id': self.upload.id, 'user-id': self.second_user.id}
        before_count = Notification.objects.count()
        response = self.client.post(share_files_url, data)
        self.assertEqual(response.status_code, 302)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIsNotNone(Notification.objects.filter(user=self.user))

    def test_process_notification_deletes_single_notification(self):
        """Goes to the process_notification view, and checks if the notification is deleted when its id is passed to it"""
        delete_url = reverse('process_notification')
        context={'notification_id': self.notification.id}
        before_count = Notification.objects.count()
        self.client.get(delete_url, context)
        after_count = Notification.objects.count()
        self.assertEqual(before_count - 1, after_count)

    def test_process_notification_deletes_all_notifications(self):
        """Goes to the process_notification view, and checks if all notifications are deleted when delete-all is passed in"""
        delete_url = reverse('process_notification')
        context={'notification_id': 'delete-all'}
        self.client.get(delete_url, context)
        after_count = Notification.objects.count()
        self.assertEqual(after_count, 0)
    
    