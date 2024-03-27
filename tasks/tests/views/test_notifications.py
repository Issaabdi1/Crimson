"""Tests of the Notifications side bar."""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from tasks.models import User, Notification, SharedFiles, Upload, Comment, VoiceComment, Team
from django.utils import timezone
import json, base64


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
        self.notification = Notification.objects.create(upload=self.upload, shared_file_instance=shared_file, time_of_notification=timezone.now(), user=self.user)
        self.notification2 = Notification.objects.create(upload=self.upload, shared_file_instance=shared_file, time_of_notification=timezone.now(), user=self.user)
        self.comment = Comment.objects.create(
            upload=self.upload,
            mark_id=1,
            commenter=self.user,
            date=timezone.now(),
            text="Test Comment 1",
        )
        #Create test voice comment and voice comment list
        self.mock_audio1 = SimpleUploadedFile('test_audio.wav', '')
        self.voice_comment = VoiceComment.objects.create(
            user=self.user,
            upload=self.upload,
            mark_id=1,
            audio=self.mock_audio1,
        )
        self.mock_audio2 = SimpleUploadedFile('test_audio.wav', b'test content 1')
        self.encoded_audio = base64.b64encode(self.mock_audio2.read()).decode()
        self.transcript = "test transcript 1"
        self.voice_comment_list = {
            1: [
                {"blob": self.encoded_audio, "transcript": self.transcript}, 
            ],
        }

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
    
    def test_notification_created_when_comment_made(self):
        """Creates a comment, and tests if a notification is created"""
        context = {
            'mark_id' : 0, 
            'upload_id' : self.upload.id, 
            'text' : "Test Comment",
        }
        create_comment_url = reverse('save_comment')
        before_count = Notification.objects.count()
        response = self.client.post(create_comment_url, context)
        self.assertEqual(response.status_code, 200)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIsNotNone(Notification.objects.filter(user=self.user))
    
    def test_notification_created_when_comment_resolved(self):
        """Shares a file, and tests if a notification is created"""
        context = {
            'for_tests': True,
            'comment_id' : self.comment.id, 
            'upload_id' : self.upload.id, 
            'resolved' : True,
        }
        update_comment_url = reverse('update_comment_status')
        before_count = Notification.objects.count()
        response = self.client.post(update_comment_url, context, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIsNotNone(Notification.objects.filter(user=self.user))
    

    def test_notification_created_when_voice_comment_made(self):
        """Shares a file, and tests if a notification is created"""
        save_voice_comments_url = reverse('save_voice_comments')
        voice_comment_str = json.dumps(self.voice_comment_list)
        before_count = Notification.objects.count()
        response = self.client.post(save_voice_comments_url, {'voice-comment-list':voice_comment_str, 'upload_id':self.upload.id})
        self.assertEqual(response.status_code, 200)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIsNotNone(Notification.objects.filter(user=self.user))
    
    def test_notification_created_when_voice_comment_resolved(self):
        """Shares a file, and tests if a notification is created"""
        resolve_voice_comment_url = reverse('mark_as_resolved')
        before_count = Notification.objects.count()
        response = self.client.post(resolve_voice_comment_url, {'audio_url': self.voice_comment.audio.url})
        self.assertEqual(response.status_code, 200)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIsNotNone(Notification.objects.filter(user=self.user))

    def test_notification_created_when_file_shared_to_team(self):
        """Shares a file to a team, and tests if notifications created for other team members"""
        self.team = Team.objects.create(name="test team")
        self.team.members.add(self.user)
        self.team.members.add(self.second_user)
        self.form_input = {'share-file': 'True', 'file-id': self.upload.id}
        before_count = Notification.objects.count()
        response = self.client.post(reverse('team_detail', kwargs={'team_id': 1}), self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIsNotNone(Notification.objects.filter(user=self.second_user))

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

    def test_delete_not_existed_notification(self):
        delete_url = reverse('process_notification_delete')
        context = {'notification_id': ''}
        before_count = Notification.objects.count()
        response = self.client.get(delete_url, context)
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(len(response.json()['notifications']), 2)