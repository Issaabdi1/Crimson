"""Tests of the Notifications side bar."""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from tasks.models import User, Notification, SharedFiles, Upload
from datetime import datetime

class NotificationsTestCase(TestCase):
    """Tests of the Notifications side bar."""

    #Test that the notifications appear on the place
    #test that when the button is clicked, it deletes the notification
    #test the delete-all button
    #test json response from view
    
    fixtures = ['tasks/tests/fixtures/default_user.json', 'tasks/tests/fixtures/other_users.json']

    def setUp(self):
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")
        second_user = User.objects.get(username="@janedoe")
        file_content = b'Test file content'
        mock_file = SimpleUploadedFile(f'test_file_0.pdf', file_content)
        shared_file = SharedFiles.objects.create(shared_file= mock_file, shared_by = second_user, shared_to = self.user)
        self.upload = Upload.objects.create(owner=self.user, file=mock_file)
        self.notification = Notification.objects.create(shared_file_instance=shared_file, time_of_notification=datetime.now(), user=self.user)

    def test_notifications_passed_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        notifications = response.context['notifications']
        self.assertIn(self.notification, notifications)

    def test_notification_created_when_file_shared(self):
        share_files_url = reverse('share_file')
        data = {'file_id': self.upload.id, 'user-id': self.user}
        before_count = Notification.objects.count()
        response = self.client.post(share_files_url, data)
        self.assertEqual(response.status_code, 200)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIsNotNone(Notification.objects.filter(user=self.user))


    def test_delete_notification_button(self):
        self.url = ""
        #test clicking the delete of the first button
        #assert that the notification is deleted, and it is not there anymore in the view (hidden)

    def test_dismiss_all_notifications_button(self):
        self.url = ""
        #test when clicking this button that all notifications are deleted, and that the button is hidden

    