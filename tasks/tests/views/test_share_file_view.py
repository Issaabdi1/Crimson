from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from tasks.models import User, Upload, SharedFiles
from tasks.tests.helpers import reverse_with_next

class ShareFileViewTestCase(TestCase):

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.url = reverse('share_file')
        self.user = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')
        self.form_input = {
            'file-id': 1,
            'user-ids': [2]
        }
        self.test_file = SimpleUploadedFile(
            'test_file.pdf',
            b'Test file content',
            content_type='text/plain'
        )

    def tearDown(self):
        if User.objects.all():
            User.objects.all().delete()

    def test_share_file_url(self):
        self.assertEqual(self.url,'/share_file/')

    def test_get_share_file(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_file.html')

    def test_get_share_file_redirects_when_not_logged_in(self):
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')
    
    def test_user_given_reminder_to_upload_before_sharing(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.WARNING)

    def test_successful_file_share(self):
        upload = Upload.objects.create(
            file=self.test_file,
            owner=self.user,
        )
        self.client.login(username=self.user.username, password='Password123')
        before_count = SharedFiles.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = SharedFiles.objects.count()
        self.assertEqual(after_count, before_count + 1)
        # response_url = reverse('filelist')
        # self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200)
        upload.delete()
    
    def test_unsuccessful_file_share_if_file_is_missing(self):
        upload = Upload.objects.create(
            file=self.test_file,
            owner=self.user,
        )
        self.client.login(username=self.user.username, password='Password123')
        before_count = SharedFiles.objects.count()
        del self.form_input['file-id']
        response = self.client.post(self.url, self.form_input)
        after_count = SharedFiles.objects.count()
        self.assertEqual(after_count, before_count)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertEqual(str(messages_list[0]), f'Please select a file to share.')  # The message isn't added before
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_file.html')
        upload.delete()
    
    def test_unsuccessful_file_share_if_file_has_been_shared_already(self):
        # Simulate sharing a file first
        upload = Upload.objects.create(
            file=self.test_file,
            owner=self.user,
        )
        self.client.login(username=self.user.username, password='Password123')
        self.client.post(self.url, self.form_input)

        # Share the same file again
        before_count = SharedFiles.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = SharedFiles.objects.count()
        self.assertEqual(after_count, before_count)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_file.html')
        upload.delete()

    def test_unsuccessful_file_share_if_file_and_user_both_not_selected(self):
        upload = Upload.objects.create(
            file=self.test_file,
            owner=self.user,
        )
        self.client.login(username=self.user.username, password='Password123')
        before_count = SharedFiles.objects.count()
        response = self.client.post(self.url, {}, follow=True)
        after_count = SharedFiles.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_file.html')
        upload.delete()