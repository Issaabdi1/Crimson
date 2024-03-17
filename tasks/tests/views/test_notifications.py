"""Tests of the Notifications side bar."""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from tasks.models import User, Notification, SharedFiles, Upload
from django.utils import timezone

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
        self.notification = Notification.objects.create(shared_file_instance=shared_file, time_of_notification=timezone.now(), user=self.user)
        self.notification2 = Notification.objects.create(shared_file_instance=shared_file, time_of_notification=timezone.now(), user=self.user)

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()

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
        data = {'file-id': self.upload.id, 'user-ids': [self.second_user.id]}
        before_count = Notification.objects.count()
        response = self.client.post(share_files_url, data)
        self.assertEqual(response.status_code, 200)  # Fix to 200, because the actual statu is 200, there isn't a redirect after share
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIsNotNone(Notification.objects.filter(user=self.user))
    
    def test_notification_created_when_file_unshared(self):
        """Shares a file, and tests if a notification is created"""
        unshare_files_url = reverse('unshare_file', kwargs={'upload_id':self.upload.id, 'user_id':self.second_user.id})
        before_count = Notification.objects.count()
        response = self.client.post(unshare_files_url)
        self.assertEqual(response.status_code, 302)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIsNotNone(Notification.objects.filter(user=self.user))

    def test_process_notification_delete_view_deletes_single_notification(self):
        """Goes to the process_notification view, and checks if the notification is deleted when its id is passed to it"""
        delete_url = reverse('process_notification_delete')
        context={'notification_id': self.notification.id}
        before_count = Notification.objects.count()
        self.client.get(delete_url, context)
        after_count = Notification.objects.count()
        self.assertEqual(before_count - 1, after_count)

    def test_process_notification_delete_view_deletes_all_notifications(self):
        """Goes to the process_notification view, and checks if all notifications are deleted when delete-all is passed in"""
        delete_url = reverse('process_notification_delete')
        context={'notification_id': 'delete-all'}
        self.client.get(delete_url, context)
        after_count = Notification.objects.count()
        self.assertEqual(after_count, 0)
    
    def test_set_notifications_as_read_view(self):
        """Test all notifications are set to read when the view is reached"""
        set_notifications_read_url = reverse('set_notifications_as_read')
        before_read_count = Notification.objects.filter(read=True).count()
        self.assertEqual(before_read_count, 0)
        self.client.get(set_notifications_read_url)
        after_read_count = Notification.objects.filter(read=True).count()
        self.assertEqual(after_read_count, 2)
    
    def test_test_mode(self):
        url = reverse('process_notification_delete')
        response = self.client.get(url, {'for_tests': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Notification.objects.filter(user=self.user).count(), 2)
        self.assertEqual(response.json()['notifications'], [])

    def test_delete_specific_notification(self):
        self.client.force_login(self.user)
        url = reverse('process_notification_delete')
        before_count = Notification.objects.count()
        response = self.client.get(url, {'for_tests': False})
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
    