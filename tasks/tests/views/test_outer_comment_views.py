import os

from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages

from tasks.models import User, Upload
from tasks.tests.helpers import reverse_with_next


class OuterCommentViewsTestCase(TestCase):
    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        os.environ['USE_S3'] = 'TRUE'
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('outer_comment_views', args=[1])
        self.uploaded_file = SimpleUploadedFile("file.pdf", b"content", content_type="application/pdf")
        self.upload = Upload.objects.create(file=self.uploaded_file, owner=self.user)

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()

    def log_in(self):
        self.client.login(username='@johndoe', password='Password123')

    def test_get_outer_comment(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('filelist')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_outer_comment_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_outer_comment_views_post(self):
        self.client.login(username='@johndoe', password='Password123')
        comments_data = {'comments': 'Test comment'}
        response = self.client.post(reverse('outer_comment_views', args=[self.upload.id]), comments_data)

        self.assertEqual(response.status_code, 302)  # Check if redirect happened
        self.assertRedirects(response, reverse('filelist'))  # Check if redirected to 'filelist' page

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Check if a message is sent
        self.assertEqual(str(messages[0]), 'Comments saved successfully.')  # Check if success message sent

        updated_upload = Upload.objects.get(id=self.upload.id)
        self.assertEqual(updated_upload.comments, 'Test comment')  # Check if comments updated correctly

    def test_unsuccessful_outer_comment_views_post(self):
        self.client.login(username='@johndoe', password='Password123')
        comments_data = {'comments': 'Test comment'}
        response = self.client.post(reverse('outer_comment_views', args=[999]), comments_data, follow=True)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertEqual(str(messages_list[0]), f'Upload not found.')

    def test_outer_comment_views_post_no_comments(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('outer_comment_views', args=[self.upload.id]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('filelist'))
        messages = list(get_messages(response.wsgi_request))

        if messages:  # Check if there are any messages
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), 'Comments saved successfully.')

        updated_upload = Upload.objects.get(id=self.upload.id)
        self.assertEqual(updated_upload.comments, '')

    def test_post_outer_comment_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(reverse('outer_comment_views', args=[self.upload.id]), {})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
